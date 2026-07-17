"""django-elastic: map and index Django models in Elasticsearch.

Importing this package wires the ``post_save``/``post_delete`` signal
receivers defined in :mod:`delastic.tasks`.
"""

from .tasks import *  # noqa: F401,F403
