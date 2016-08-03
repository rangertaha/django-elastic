#!/usb/bin/env python
# -*- coding:utf-8-*-
"""

"""
import time

from django.core.management.base import BaseCommand, CommandError

from delastic.indexer import ModelIndex


class Command(BaseCommand):
    """ Indexes the django models in elasticesearch

    """
    help = __doc__

    def index_model(self, model):
        self.stdout.write(
            'Indexing: {0} - {1}...'.format(
                model.objects.count(), model.__name__))
        for model in model.objects.all():
            indexer = ModelIndex.indexer_for_instance(model)
            if indexer is not None:
                indexable_func = getattr(indexer, 'indexable', None)
                if callable(indexable_func):
                    if indexable_func():
                        indexer.save()
                    else:
                        indexer.delete()
                else:
                    indexer.save()

    def handle(self, **options):
        model_types = ModelIndex.registry.keys()
        for model in model_types:
            if not isinstance(model, str):
                self.index_model(model)
