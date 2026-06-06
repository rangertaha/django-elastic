# -*- coding: utf-8 -*-
"""

"""
from django.conf import settings

PROJECT_SETTINGS = getattr(settings, 'DJANGO_ELASTIC', None)

DJANGO_ELASTIC = {
    'hosts': ['localhost'],
    'port': 9200,
    'scheme': 'http',
    'index': 'django',
}

if PROJECT_SETTINGS:
    DJANGO_ELASTIC.update(PROJECT_SETTINGS)


def elastic_hosts():
    """Normalise the configured hosts into the node URLs expected by the
    elasticsearch 8.x/9.x client (e.g. ``http://localhost:9200``)."""
    scheme = DJANGO_ELASTIC.get('scheme', 'http')
    port = DJANGO_ELASTIC.get('port', 9200)
    nodes = []
    for host in DJANGO_ELASTIC.get('hosts', []):
        if '://' in host:
            nodes.append(host)
        else:
            nodes.append('{0}://{1}:{2}'.format(scheme, host, port))
    return nodes
