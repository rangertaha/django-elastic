#!/usb/bin/env python
# -*- coding:utf-8-*-
"""

"""
from django.core.management.base import BaseCommand

from delastic.indexer import ModelIndex


class Command(BaseCommand):
    """

NAME
     create_elastic_mapping -- Deletes the index and creates a new mapping


DESCRIPTION
     ...


EXAMPLE
    ...


    """
    help = __doc__

    def handle(self, *args, **options):
        pass
