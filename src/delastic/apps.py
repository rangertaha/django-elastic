"""Django application configuration for django-elastic."""

from django.apps import AppConfig


class ElasticConfig(AppConfig):
    name = "delastic"

    def ready(self):
        pass
