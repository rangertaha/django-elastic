"""Delete the index and create a new mapping in Elasticsearch.

.. warning::
    Not implemented yet. Running this command is currently a no-op; the
    mapping is created lazily by the indexers instead. Kept as a stub so
    the documented command name remains stable.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Deletes the index and creates a new mapping (not implemented yet)."""

    help = __doc__

    def handle(self, *args, **options):
        # TODO: rebuild the Elasticsearch mapping from the indexer registry
        # (see delastic.indexer.IndexMeta.init). Intentionally a no-op for
        # now -- flagged rather than implemented.
        pass
