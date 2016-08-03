# -*- coding: utf-8 -*-
from django.forms import ModelForm
from delastic.registration import ModelIndex

from .models import Article


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'desc', 'created']
