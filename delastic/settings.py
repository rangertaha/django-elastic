# -*- coding: utf-8 -*-
"""

"""
from django.conf import settings

PROJECT_SETTINGS = getattr(settings, 'DJANGO_ELASTIC', None)

DJANGO_ELASTIC = {
    'hosts': ['localhost'],
    'port': 9200,
    'index': 'django',
}

if PROJECT_SETTINGS:
    DJANGO_ELASTIC.update(PROJECT_SETTINGS)
