from django.db import models


class Article(models.Model):
    """Model used to exercise the model-to-document mapping."""

    title = models.CharField(max_length=500, blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    views = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        app_label = "testapp"

    def __str__(self):
        return self.title or ""


class Plain(models.Model):
    """Model with no indexer registered against it."""

    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = "testapp"
