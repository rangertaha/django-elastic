# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
from django.dispatch import receiver
from delastic.indexer import ModelIndex
from elasticsearch_dsl import (
    DocType, String, Integer, Date, Boolean, GeoShape, Long, Nested,
    InnerObjectWrapper)

from delastic.signals import pre_index

from .models import Article


class ArticleIndex(ModelIndex):
    title = String(multi=True, index='analyzed', analyzer='keyword')
    desc = String()

    class Meta:
        model = Article
        #client = Elasticsearch()
        #index = 'news'
        #doc_type = 'article'
        fields = ['title', 'desc', 'created']
        exclude = ['image']

    def clean_title(self):
        return getattr(self.instance, 'title')

    def indexable(self):
        return self.instance.active


@receiver(pre_index)
def pre_index_handler(sender, instance, **kwargs):
    """Signal intercept before indexing"""

    #print 'Django Instance: ', instance
    import json
    #print 'Mapping: ', json.dumps(sender._meta.mapping.to_dict(), indent=4)
    pass

