from django.urls import path
from articles import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.ArticlesRetrieveView.as_view(), name='articles'),
    path('authors/', views.AuthorsRetrieveView.as_view(), name='authors'),
    path('categories/', views.CategoriesRetrieveView.as_view(), name='categories'),
    path('outlets/', views.OutletsRetrieveView.as_view(), name='outlets'),
]