from articles.models import Author, Outlet, Category, Article

from django_filters import rest_framework as filters

class ArticleFilter(filters.FilterSet):
    """Adds filtering to articles."""
    date = filters.DateTimeFromToRangeFilter()
    authors = filters.ModelMultipleChoiceFilter(
        queryset=Author.objects.all()
    )
    outlet = filters.ModelMultipleChoiceFilter(
        queryset=Outlet.objects.all()
    )
    categories = filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Article
        fields = {
            'title': ['contains', 'endswith', 'startswith'],
            'date': [],
            'authors': [],
            'outlet': [],
            'categories': []
        }


class AuthorFilter(filters.FilterSet):
    """Adds filtering to authors."""
    outlet = filters.ModelMultipleChoiceFilter(
        queryset=Outlet.objects.all()
    )

    class Meta:
        model = Author
        fields = {
            'name': ['contains'],
            'about': ['contains'],
            'facebook': ['contains'],
            'twitter': ['contains'],
            'linkedin': ['contains'],
            'profile': ['contains'],
            'website': ['contains'],
            'outlet': [],
        }


class CategoryFilter(filters.FilterSet):
    """Adds filtering to categories."""

    class Meta:
        model = Category
        fields = {
            'name': ['contains'],
        }


class OutletFilter(filters.FilterSet):
    """Adds filtering to outlets."""

    class Meta:
        model = Outlet
        fields = {
            'name': ['contains'],
            'website': ['contains'],
            'description': ['contains'],
        }