"""Tests for delastic.indexer with a mocked Elasticsearch client."""

from datetime import datetime
from unittest import mock

import pytest
from django.db import models
from elasticsearch.dsl import Date, Mapping, Search, Text

from delastic import indexer as indexer_module
from delastic.indexer import ModelIndex, default_client
from delastic.signals import post_delete, post_index, pre_delete, pre_index
from tests.testapp.indexers import ArticleIndex
from tests.testapp.models import Article, Plain


class TestRegistry:
    def test_model_registered(self):
        assert ModelIndex.registry[Article] is ArticleIndex

    def test_doc_type_defaults_to_snake_case_class_name(self):
        assert ArticleIndex._meta.doc_type == "article_index"
        assert isinstance(ModelIndex.registry["article_index"], Mapping)

    def test_indexer_for_model(self):
        assert ModelIndex.indexer_for_model(Article) is ArticleIndex
        assert ModelIndex.indexer_for_model(Plain) is None

    def test_indexer_for_instance(self):
        instance = Article(title="hello")
        indexer = ModelIndex.indexer_for_instance(instance)
        assert isinstance(indexer, ArticleIndex)
        assert indexer.instance is instance

    def test_indexer_for_instance_unregistered_model(self):
        assert ModelIndex.indexer_for_instance(Plain(name="x")) is None

    def test_meta_options(self):
        meta = ArticleIndex._meta
        assert meta.model is Article
        assert meta.index == "test-articles"
        assert meta.fields == ["title", "desc", "created"]
        assert meta.exclude == ["url"]


class TestMapping:
    def test_mapping_built_from_model_fields(self):
        # CharField/TextField -> text, DateTimeField -> date; other field
        # types are not auto-mapped.
        fields = ArticleIndex.fields
        assert fields["title"]["type"] == "text"
        assert fields["desc"]["type"] == "text"
        assert fields["created"]["type"] == "date"
        assert "url" not in fields  # URLField is not auto-translated
        assert "views" not in fields
        assert "active" not in fields

    def test_indexer_field_overrides_model_mapping(self):
        # ArticleIndex declares title = Text(analyzer="keyword").
        assert ArticleIndex.fields["title"]["analyzer"] == "keyword"

    def test_translate_field(self):
        name, dsl = ArticleIndex._translate_field(Article._meta.get_field("title"))
        assert (name, dsl) == ("title", Text)

        name, dsl = ArticleIndex._translate_field(Article._meta.get_field("created"))
        assert (name, dsl) == ("created", Date)

        # Untranslatable fields return (None, None).
        assert ArticleIndex._translate_field(Article._meta.get_field("active")) == (
            None,
            None,
        )
        assert ArticleIndex._translate_field(models.SlugField(name="s")) == (
            None,
            None,
        )

    def test_init_saves_mapping_through_client(self, es_client):
        with mock.patch.object(Mapping, "save") as save:
            ArticleIndex.init()
        save.assert_called_once_with("test-articles", using=es_client)


class TestDocumentCleaning:
    def test_clean_uses_clean_methods_and_instance_attrs(self):
        instance = Article(title="  Hello  ", desc="Body")
        indexer = ArticleIndex(instance)
        # clean_title() strips whitespace; desc/created come straight from
        # the instance.
        assert indexer.record["title"] == "Hello"
        assert indexer.record["desc"] == "Body"
        assert indexer.record["created"] is None

    def test_no_instance_no_record(self):
        indexer = ArticleIndex()
        assert indexer.record == {}
        assert indexer.instance is None

    def test_timestamp_is_timezone_aware(self):
        ts = ArticleIndex(Article(title="x")).timestamp()
        assert isinstance(ts, datetime)
        assert ts.tzinfo is not None


@pytest.mark.django_db
class TestSaveDelete:
    def test_save_indexes_document(self, es_client):
        article = Article.objects.create(title=" Title ", desc="Body")
        es_client.reset_mock()

        indexer = ArticleIndex(article)
        indexer.save()

        es_client.index.assert_called_once()
        kwargs = es_client.index.call_args.kwargs
        assert kwargs["index"] == "test-articles"
        assert kwargs["id"] == article.pk
        document = kwargs["document"]
        assert document["title"] == "Title"
        assert document["desc"] == "Body"
        assert document["timestamp"].tzinfo is not None

    def test_save_sends_signals(self, es_client):
        article = Article.objects.create(title="x")
        seen = []

        def on_pre(sender, **kwargs):
            seen.append("pre")

        def on_post(sender, **kwargs):
            seen.append("post")

        pre_index.connect(on_pre)
        post_index.connect(on_post)
        try:
            ArticleIndex(article).save()
        finally:
            pre_index.disconnect(on_pre)
            post_index.disconnect(on_post)
        assert seen == ["pre", "post"]

    def test_delete_removes_document(self, es_client):
        article = Article.objects.create(title="x")
        es_client.reset_mock()

        ArticleIndex(article).delete()

        es_client.delete.assert_called_once()
        kwargs = es_client.delete.call_args.kwargs
        assert kwargs["index"] == "test-articles"
        assert kwargs["id"] == article.pk

    def test_delete_swallows_client_errors(self, es_client):
        article = Article.objects.create(title="x")
        es_client.delete.side_effect = Exception("boom")
        seen = []

        def on_pre(sender, **kwargs):
            seen.append("pre")

        def on_post(sender, **kwargs):
            seen.append("post")

        pre_delete.connect(on_pre)
        post_delete.connect(on_post)
        try:
            # Must not raise, and must still emit both signals.
            ArticleIndex(article).delete()
        finally:
            pre_delete.disconnect(on_pre)
            post_delete.disconnect(on_post)
        assert seen == ["pre", "post"]

    def test_clean_id_sets_content_type(self, es_client):
        article = Article.objects.create(title="x")
        indexer = ArticleIndex(article)
        assert indexer.clean_id() == article.pk
        assert indexer.django_id == str(article.pk)
        assert indexer.content_type.model_class() is Article


class TestSearch:
    def test_search_uses_meta_client_and_index(self, es_client):
        search = ArticleIndex.search()
        assert isinstance(search, Search)
        assert search._index == ["test-articles"]
        assert search._using is es_client

    def test_search_accepts_overrides(self):
        other = mock.MagicMock(name="other-client")
        search = ArticleIndex.search(es=other, index="other-index")
        assert search._index == ["other-index"]
        assert search._using is other


def test_default_client_uses_configured_hosts():
    with mock.patch.object(indexer_module, "Elasticsearch") as es_cls:
        default_client()
    es_cls.assert_called_once_with(hosts=["http://localhost:9200"])
