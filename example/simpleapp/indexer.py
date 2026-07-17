from django.dispatch import receiver
from elasticsearch.dsl import Text

from delastic.indexer import ModelIndex
from delastic.signals import pre_index

from .models import Article


class ArticleIndex(ModelIndex):
    title = Text(multi=True, analyzer="keyword")
    desc = Text()

    class Meta:
        model = Article
        # client = Elasticsearch()
        # index = 'news'
        # doc_type = 'article'
        fields = ["title", "desc", "created"]
        exclude = ["image"]

    def clean_title(self):
        return self.instance.title

    def indexable(self):
        return self.instance.active


@receiver(pre_index)
def pre_index_handler(sender, instance, **kwargs):
    """Signal intercept before indexing"""
    # print('Django Instance: ', instance)
