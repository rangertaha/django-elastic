"""Tests for the post_save/post_delete receivers in delastic.tasks."""

import pytest

from tests.testapp.models import Article, Plain

pytestmark = pytest.mark.django_db


def test_saving_indexable_instance_indexes_it(es_client):
    article = Article.objects.create(title="Fresh", active=True)

    es_client.index.assert_called_once()
    assert es_client.index.call_args.kwargs["id"] == article.pk
    es_client.delete.assert_not_called()


def test_saving_non_indexable_instance_deletes_it(es_client):
    # ArticleIndex.indexable() returns False when active is False, so a
    # save must remove any stale document instead of indexing it.
    Article.objects.create(title="Hidden", active=False)

    es_client.index.assert_not_called()
    es_client.delete.assert_called_once()


def test_deleting_instance_removes_document(es_client):
    article = Article.objects.create(title="Doomed", active=True)
    es_client.reset_mock()

    article.delete()

    es_client.delete.assert_called_once()
    es_client.index.assert_not_called()


def test_unregistered_model_is_ignored(es_client):
    plain = Plain.objects.create(name="nothing to see")
    plain.delete()

    es_client.index.assert_not_called()
    es_client.delete.assert_not_called()
