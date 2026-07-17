from django.views.generic import ListView

from delastic.indexer import ModelIndex

# Imported for its side effect: defining ArticleIndex registers it with the
# ModelIndex registry so the article model gets indexed.
from .indexer import ArticleIndex  # noqa: F401
from .models import Article


class NewsSearch(ListView):
    model = Article

    index = "news"
    doc_types = ["feed", "feed_item", "person"]
    filters = []
    sort = []
    paginate_by = 10
    form = "SearchForm"

    def get_queryset(self):
        print(ModelIndex.registry)
        return Article.objects.all()
