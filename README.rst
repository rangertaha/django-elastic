django-elastic
==============

* Simple way to index/delete/update django models
* Queries Elasticsearch only, not hitting the Django database
* Define the mapping with elasticsearch-dsl, defaults to basic field types.
* Override field values.
* Define if a model instance should be index or not


TODO:

* Search view:
    * Elasticsearch based pagination
    * Elasticsearch-dsl queries
    * Adds search filters and possible values in the template context

* Support multiple models per doc_type



Requirements
------------

* elasticsearch-dsl


Installation
------------

.. code-block:: bash

    pip install django-elastic


Settings
--------

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'delastic',
    )

Optional elasticsearch settings, Defaults to the following


.. code-block:: python

    DJANGO_ELASTIC = {
        'hosts': ['localhost'],
        'port': 9200,
        'index': 'django',
    }


Model
-----

An example model

.. code-block:: python

    class Article(models.Model):
        title = models.CharField(max_length=500, blank=True, null=True)
        desc = models.TextField(blank=True, null=True)
        created = models.DateTimeField(blank=True, null=True)
        updated = models.DateTimeField(blank=True, null=True)
        image = models.URLField(max_length=500, blank=True, null=True)
        url = models.URLField(max_length=500, blank=True, null=True)
        active = models.BooleanField(default=True)

        def __unicode__(self):
            return self.title


Indexer
-------


The simplest example of an indexer for the model.

.. code-block:: python

    from delastic.indexer import ModelIndex

    class ArticleIndex(ModelIndex):
        class Meta:
            model = Article

Or for more control

.. code-block:: python

    from delastic.indexer import ModelIndex

    class ArticleIndex(ModelIndex):
        title = String(multi=True, index='analyzed', analyzer='keyword')
        desc = String()

        class Meta:
            model = Article
            client = Elasticsearch()
            index = 'news'
            doc_type = 'article'
            fields = ['title', 'desc', 'created']
            exclude = ['image']

        # Clean/Modify the 'title' field before indexing in elasticsearch
        # functions that start with 'clean_' followed by the field name of
        # a the model.
        def clean_title(self):
            return getattr(self.instance, 'title')

        # If this returns False, it does not index the instance
        def indexable(self):
            return self.instance.active


View
----


TODO...



Management Commands
-------------------

Create mapping in elasticsearch

.. code-block:: bash

    ./manage.py create_elastic_mapping


Index models in elasticsearch


.. code-block:: bash

    ./manage.py create_elastic_index


