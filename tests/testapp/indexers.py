"""Indexers used by the test suite.

The Elasticsearch client is a ``MagicMock`` -- no test ever talks to a live
cluster.
"""

from unittest import mock

from elasticsearch.dsl import Text

from delastic.indexer import ModelIndex

from .models import Article

MOCK_ES = mock.MagicMock(name="mock-elasticsearch-client")


class ArticleIndex(ModelIndex):
    title = Text(analyzer="keyword")

    class Meta:
        model = Article
        client = MOCK_ES
        index = "test-articles"
        fields = ["title", "desc", "created"]
        exclude = ["url"]

    def clean_title(self):
        return (self.instance.title or "").strip()

    def indexable(self):
        return self.instance.active
