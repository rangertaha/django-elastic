# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Article


@admin.register(Article)
class AuthorAdmin(admin.ModelAdmin):
    pass
