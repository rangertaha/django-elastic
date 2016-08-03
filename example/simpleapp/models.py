# -*- coding: utf-8 -*-
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)

    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title
