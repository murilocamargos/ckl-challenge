from articles.models import Author, Outlet, Category, Article

from django_filters import rest_framework as filters

class ArticleFilter(filters.FilterSet):
    """Adds filtering to articles."""
    date = filters.DateTimeFromToRangeFilter()
    authors = filters.ModelMultipleChoiceFilter(
        queryset = Author.objects.all()
    )
    outlet = filters.ModelMultipleChoiceFilter(
        queryset = Outlet.objects.all()
    )
    categories = filters.ModelMultipleChoiceFilter(
        queryset = Category.objects.all()
    )

    class Meta:
        model = Article
        fields = {
            'title': ['exact', 'contains', 'endswith', 'startswith'],
            'date': [],
            'authors': [],
            'outlet': [],
            'categories': []
        }