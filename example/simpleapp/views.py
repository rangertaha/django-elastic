# -*- coding: utf-8 -*-
from django.views.generic import ListView
from delastic.indexer import ModelIndex

from .models import Article
from .indexer import ArticleIndex


class NewsSearch(ListView):
    model = Article

    index = 'news'
    doc_types = ['feed', 'feed_item', 'person']
    filters = []
    sort = []
    paginate_by = 10
    form = 'SearchForm'

    def get_queryset(self):
        print ModelIndex.registry
        return Article.objects.all()
