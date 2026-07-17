django-elastic
==============

.. image:: https://github.com/rangertaha/django-elastic/actions/workflows/ci.yml/badge.svg
    :target: https://github.com/rangertaha/django-elastic/actions/workflows/ci.yml
    :alt: CI status

.. image:: https://img.shields.io/pypi/v/django-elastic.svg
    :target: https://pypi.org/project/django-elastic/
    :alt: PyPI version

.. image:: https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue.svg
    :target: https://pypi.org/project/django-elastic/
    :alt: Supported Python versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/rangertaha/django-elastic/blob/master/LICENSE
    :alt: MIT License

Django model mapping and a flexible indexer for Elasticsearch. Declare an
indexer per model and django-elastic keeps the Elasticsearch index in sync
automatically on every save and delete.

* Simple way to index/delete/update Django models
* Queries Elasticsearch only, without hitting the Django database
* Builds the mapping from the model's fields by default; override any field
  with ``elasticsearch.dsl`` field types
* Clean/override field values before indexing (``clean_<field>`` methods)
* Decide per instance whether it should be indexed (``indexable()``)

Requires Python 3.12+, Django 5.2, and the ``elasticsearch`` 9.x client
(the DSL is bundled as ``elasticsearch.dsl``).


Installation
------------

.. code-block:: bash

    pip install django-elastic


Quickstart
----------

Add ``delastic`` to your ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'delastic',
    )

Optionally configure the Elasticsearch connection (the defaults are shown):

.. code-block:: python

    DJANGO_ELASTIC = {
        'hosts': ['localhost'],
        'port': 9200,
        'scheme': 'http',
        'index': 'django',
    }

Given a model:

.. code-block:: python

    class Article(models.Model):
        title = models.CharField(max_length=500, blank=True, null=True)
        desc = models.TextField(blank=True, null=True)
        created = models.DateTimeField(blank=True, null=True)
        updated = models.DateTimeField(blank=True, null=True)
        image = models.URLField(max_length=500, blank=True, null=True)
        url = models.URLField(max_length=500, blank=True, null=True)
        active = models.BooleanField(default=True)

        def __str__(self):
            return self.title or ''

the simplest indexer is:

.. code-block:: python

    from delastic.indexer import ModelIndex

    class ArticleIndex(ModelIndex):
        class Meta:
            model = Article

From then on, saving or deleting an ``Article`` updates Elasticsearch
automatically via ``post_save``/``post_delete`` signal receivers.


Indexer options
---------------

For more control:

.. code-block:: python

    from elasticsearch import Elasticsearch
    from elasticsearch.dsl import Text

    from delastic.indexer import ModelIndex

    class ArticleIndex(ModelIndex):
        title = Text(multi=True, analyzer='keyword')
        desc = Text()

        class Meta:
            model = Article
            client = Elasticsearch('http://localhost:9200')
            index = 'news'
            fields = ['title', 'desc', 'created']
            exclude = ['image']

        # Clean/modify the 'title' field before indexing. Methods named
        # 'clean_<field>' override the model attribute of the same name.
        def clean_title(self):
            return self.instance.title

        # If this returns False, the instance is not indexed (and any
        # existing document for it is removed from the index).
        def indexable(self):
            return self.instance.active

Search through the indexer with an ``elasticsearch.dsl`` ``Search`` object:

.. code-block:: python

    search = ArticleIndex.search().query('match', title='django')


Management commands
-------------------

Index all registered models in Elasticsearch:

.. code-block:: bash

    ./manage.py create_elastic_index

Create the mapping in Elasticsearch:

.. code-block:: bash

    ./manage.py create_elastic_mapping

.. note::
    ``create_elastic_mapping`` is currently a documented no-op stub; the
    mapping is built lazily by the indexers. See the roadmap below.


Signals
-------

``delastic.signals`` exposes ``pre_index``, ``post_index``, ``pre_delete``,
and ``post_delete`` so you can hook into the indexing lifecycle:

.. code-block:: python

    from django.dispatch import receiver
    from delastic.signals import pre_index

    @receiver(pre_index)
    def pre_index_handler(sender, instance, **kwargs):
        ...


Example project
---------------

A runnable demo lives in ``example/`` (an RSS-feed reader that indexes
articles). From a source checkout:

.. code-block:: bash

    cd example
    python manage.py migrate
    python manage.py get_articles
    python manage.py create_elastic_index
    python manage.py runserver


Development
-----------

.. code-block:: bash

    pip install -e . --group dev
    pytest            # Elasticsearch is mocked; no cluster needed
    ruff check . && ruff format --check .
    mypy


Roadmap
-------

* Search view (``delastic/views.py`` is an intentional placeholder):
  Elasticsearch-based pagination, ``elasticsearch.dsl`` queries, and search
  filters in the template context
* Implement ``create_elastic_mapping`` (currently a no-op stub)
* Support multiple models per index


License
-------

MIT -- see ``LICENSE``.
