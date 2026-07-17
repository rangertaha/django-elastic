"""Tests for delastic.settings."""

from unittest import mock

from delastic import settings as delastic_settings


def test_defaults_merged_with_project_settings():
    # tests/settings.py overrides only the index name; the rest fall back
    # to the library defaults.
    assert delastic_settings.DJANGO_ELASTIC["index"] == "test-index"
    assert delastic_settings.DJANGO_ELASTIC["hosts"] == ["localhost"]
    assert delastic_settings.DJANGO_ELASTIC["port"] == 9200
    assert delastic_settings.DJANGO_ELASTIC["scheme"] == "http"


def test_elastic_hosts_builds_node_urls():
    assert delastic_settings.elastic_hosts() == ["http://localhost:9200"]


def test_elastic_hosts_custom_scheme_and_port():
    overrides = {"hosts": ["es.example.com"], "scheme": "https", "port": 9243}
    with mock.patch.dict(delastic_settings.DJANGO_ELASTIC, overrides):
        assert delastic_settings.elastic_hosts() == ["https://es.example.com:9243"]


def test_elastic_hosts_passes_through_full_urls():
    overrides = {"hosts": ["https://node1:9200", "localhost"]}
    with mock.patch.dict(delastic_settings.DJANGO_ELASTIC, overrides):
        assert delastic_settings.elastic_hosts() == [
            "https://node1:9200",
            "http://localhost:9200",
        ]
