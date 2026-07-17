"""Index the registered Django models in Elasticsearch."""

from django.core.management.base import BaseCommand

from delastic.indexer import ModelIndex


class Command(BaseCommand):
    """Indexes the django models in elasticesearch"""

    help = __doc__

    def index_model(self, model):
        self.stdout.write(f"Indexing: {model.objects.count()} - {model.__name__}...")
        for instance in model.objects.all():
            indexer = ModelIndex.indexer_for_instance(instance)
            if indexer is not None:
                indexable_func = getattr(indexer, "indexable", None)
                if callable(indexable_func):
                    if indexable_func():
                        indexer.save()
                    else:
                        indexer.delete()
                else:
                    indexer.save()

    def handle(self, **options):
        model_types = ModelIndex.registry.keys()
        for model in model_types:
            if not isinstance(model, str):
                self.index_model(model)
