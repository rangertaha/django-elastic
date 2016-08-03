# -*- coding:utf-8 -*-
"""

"""
from django.dispatch import Signal

pre_index = Signal(providing_args=['instance', 'indexer'])
post_index = Signal(providing_args=['instance', 'indexer'])

pre_delete = Signal(providing_args=['instance', 'indexer'])
post_delete = Signal(providing_args=['instance', 'indexer'])

mapping_pre_index = Signal(providing_args=['instance', 'indexer'])
mapping_post_index = Signal(providing_args=['instance', 'indexer'])

mapping_pre_delete = Signal(providing_args=['instance', 'indexer'])
mapping_post_delete = Signal(providing_args=['instance', 'indexer'])
