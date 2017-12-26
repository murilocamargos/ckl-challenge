from django.contrib import admin

from articles.models import Author, Outlet, Category, Article

admin.site.register(Author)
admin.site.register(Outlet)
admin.site.register(Category)
admin.site.register(Article)