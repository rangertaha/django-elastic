Tutorial
========



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

