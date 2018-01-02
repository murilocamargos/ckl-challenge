from django.urls import path

from articles import views

urlpatterns = [
    path('', views.api, name='api'),

    path('articles/', views.ArticlesRetrieveView.as_view(), name='articles'),
    path('authors/', views.AuthorsRetrieveView.as_view(), name='authors'),
    path('categories/', views.CategoriesRetrieveView.as_view(), name='categories'),
    path('outlets/', views.OutletsRetrieveView.as_view(), name='outlets'),

    path('article/<int:pk>/', views.ArticleRUDView.as_view(), name='article'),
    path('author/<int:pk>/', views.AuthorRUDView.as_view(), name='author'),
    path('category/<int:pk>/', views.CategoryRUDView.as_view(), name='category'),
    path('outlet/<int:pk>/', views.OutletRUDView.as_view(), name='outlet'),

    path('article/', views.ArticleCreateView.as_view(), name='article-create'),
    path('author/', views.AuthorCreateView.as_view(), name='author-create'),
    path('category/', views.CategoryCreateView.as_view(), name='category-create'),
    path('outlet/', views.OutletCreateView.as_view(), name='outlet-create'),
]
