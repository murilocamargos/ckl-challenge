from rest_framework import generics
from .serializers import AuthorSerializer, OutletSerializer, CategorySerializer, ArticleSerializer
from .models import Author, Outlet, Category, Article

class AuthorsRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class ArticlesRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all articles."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    
class CategoriesRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OutletsRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all outlets."""
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer