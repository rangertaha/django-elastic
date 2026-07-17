"""Minimal Django settings for the django-elastic test suite.

No live Elasticsearch is ever contacted: every test replaces the client
with a mock (see ``tests/conftest.py``).
"""

SECRET_KEY = "test-secret-key-not-for-production"

DEBUG = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "delastic",
    "tests.testapp",
]

DJANGO_ELASTIC = {
    "hosts": ["localhost"],
    "port": 9200,
    "scheme": "http",
    "index": "test-index",
}
