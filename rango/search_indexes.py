from haystack import indexes
from rango.models import Page

class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, model_attr='title')


    def get_model(self):
        return Page

    def index_queryset(self, using=None):
        return self.get_model().objects.all()