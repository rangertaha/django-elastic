# -*- coding:utf-8 -*-
"""

"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .indexer import ModelIndex


@receiver(post_save)
def es_index_instance(sender, instance, created, **kwargs):
    """Signal receiver function for Creating/Indexing a model into
    elasticsearch

    """
    indexer = ModelIndex.indexer_for_instance(instance)
    if indexer is not None:
        indexable_func = getattr(indexer, 'indexable', None)
        if callable(indexable_func):
            if indexable_func():
                indexer.save()
            else:
                indexer.delete()
        else:
            indexer.save()


@receiver(post_delete)
def es_delete_instance(sender, instance, **kwargs):
    """Signal receiver function for removing indexed models from
    elasticsearch

    """
    indexer = ModelIndex.indexer_for_instance(instance)
    if indexer is not None:
        indexer.delete()
