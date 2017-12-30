from django.shortcuts import render

from rest_framework import generics, permissions

from articles.serializers import *
from articles.models import *
from articles.filters import *

def api(request):
    """Renders the api docs."""
    return render(request, 'index.html')



class ArticlesRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all articles."""
    queryset = Article.objects.all().order_by('-date')
    serializer_class = ArticleRetrieveSerializer
    filter_class = ArticleFilter


class AuthorsRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_class = AuthorFilter
    

class CategoriesRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_class = CategoryFilter


class OutletsRetrieveView(generics.ListAPIView):
    """This class handles the http GET, requests for showing all outlets."""
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    filter_class = OutletFilter



class IsAdminForUpdateAndDelete(permissions.BasePermission):
    """Custom permission class to allow non-admin users to retrieve an item."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method == 'GET'


class ArticleRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the http GET, PUT, PATCH and DELETE requests for articles."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsAdminForUpdateAndDelete,)

    def get_serializer_class(self):
        """If the user tries to retrieve an article, use specific serializer."""
        if self.request.method == 'GET':
            return ArticleRetrieveSerializer
        return ArticleSerializer


class AuthorRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the http GET, PUT, PATCH and DELETE requests for authors."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminForUpdateAndDelete,)


class CategoryRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the http GET, PUT, PATCH and DELETE requests for categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminForUpdateAndDelete,)


class OutletRUDView(generics.RetrieveUpdateDestroyAPIView):
    """Handles the http GET, PUT, PATCH and DELETE requests for outlets."""
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    permission_classes = (IsAdminForUpdateAndDelete,)



class ArticleCreateView(generics.CreateAPIView):
    """Handles the http POST requests for articles' creation."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAdminUser,)


class AuthorCreateView(generics.CreateAPIView):
    """Handles the http POST requests for authors' creation."""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (permissions.IsAdminUser,)


class CategoryCreateView(generics.CreateAPIView):
    """Handles the http POST requests for categories' creation."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUser,)


class OutletCreateView(generics.CreateAPIView):
    """Handles the http POST requests for outlets' creation."""
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    permission_classes = (permissions.IsAdminUser,)