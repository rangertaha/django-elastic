"""Default settings, overridable via ``DJANGO_ELASTIC`` in Django settings."""

from typing import Any

from django.conf import settings

PROJECT_SETTINGS = getattr(settings, "DJANGO_ELASTIC", None)

DJANGO_ELASTIC: dict[str, Any] = {
    "hosts": ["localhost"],
    "port": 9200,
    "scheme": "http",
    "index": "django",
}

if PROJECT_SETTINGS:
    DJANGO_ELASTIC.update(PROJECT_SETTINGS)


def elastic_hosts():
    """Normalise the configured hosts into the node URLs expected by the
    elasticsearch 8.x/9.x client (e.g. ``http://localhost:9200``)."""
    scheme = DJANGO_ELASTIC.get("scheme", "http")
    port = DJANGO_ELASTIC.get("port", 9200)
    nodes = []
    for host in DJANGO_ELASTIC.get("hosts", []):
        if "://" in host:
            nodes.append(host)
        else:
            nodes.append(f"{scheme}://{host}:{port}")
    return nodes
