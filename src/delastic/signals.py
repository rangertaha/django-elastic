"""Signals sent around indexing and deletion of documents."""

from django.dispatch import Signal

# Signal arguments (formerly declared via ``providing_args``, removed in
# Django 4.0): instance, indexer
pre_index = Signal()
post_index = Signal()

pre_delete = Signal()
post_delete = Signal()

mapping_pre_index = Signal()
mapping_post_index = Signal()

mapping_pre_delete = Signal()
mapping_post_delete = Signal()
