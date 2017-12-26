from django.http import JsonResponse

from rest_framework import generics

from articles.serializers import *
from articles.models import *
from articles.filters import *

def index(request):
    endpoints = {
        'get authors': '/authors',
        'get categories': '/categories',
        'get articles': '/articles',
        'get outlets': '/outlets',
    }

    return JsonResponse(endpoints)

class AuthorsRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class ArticlesRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all articles."""
    queryset = Article.objects.all().order_by('-date')
    serializer_class = ArticleSerializer
    filter_class = ArticleFilter
    
class CategoriesRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OutletsRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all outlets."""
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer