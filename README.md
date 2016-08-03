# UNDER DEVELOPEMNT

## django-elastic (delastic)

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



## Requirements

* elasticsearch-dsl


## Installation

    pip install django-elastic


## Settings

    INSTALLED_APPS = (
        ...
        'delastic',
    )

Optional elasticsearch settings, Defaults to the following

    DJANGO_ELASTIC = {
        'hosts': ['localhost'],
        'port': 9200,
        'index': 'django',
    }


## Model

An example model

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


## Indexer

The simplest example of an indexer for the model.

    from delastic.indexer import ModelIndex

    class ArticleIndex(ModelIndex):
        class Meta:
            model = Article


## View

TODO...




