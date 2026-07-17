"""Tests for the management commands (Elasticsearch fully mocked)."""

from io import StringIO

import pytest
from django.core.management import call_command

from tests.testapp.models import Article

pytestmark = pytest.mark.django_db


class TestCreateElasticIndex:
    def test_indexes_registered_models(self, es_client):
        indexed = Article.objects.create(title="Visible", active=True)
        Article.objects.create(title="Hidden", active=False)
        es_client.reset_mock()

        out = StringIO()
        call_command("create_elastic_index", stdout=out)

        assert "Indexing: 2 - Article" in out.getvalue()
        # One indexable instance is indexed, the non-indexable one is
        # deleted from the index.
        es_client.index.assert_called_once()
        assert es_client.index.call_args.kwargs["id"] == indexed.pk
        es_client.delete.assert_called_once()

    def test_no_instances_is_a_clean_run(self, es_client):
        es_client.reset_mock()
        out = StringIO()
        call_command("create_elastic_index", stdout=out)

        assert "Indexing: 0 - Article" in out.getvalue()
        es_client.index.assert_not_called()
        es_client.delete.assert_not_called()


class TestCreateElasticMapping:
    def test_is_a_documented_noop(self, es_client):
        # The command is a stub (see the module docstring); it must run
        # without error and without touching Elasticsearch.
        es_client.reset_mock()
        out = StringIO()
        call_command("create_elastic_mapping", stdout=out)

        es_client.index.assert_not_called()
        es_client.delete.assert_not_called()
