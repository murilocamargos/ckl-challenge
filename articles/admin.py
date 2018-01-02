from django.contrib import admin

from articles.models import Author, Outlet, Category, Article


class OutletAdmin(admin.ModelAdmin):
    """Changes outlets listing on admin panel."""
    model = Outlet
    list_display = ['name', 'active', 'website']


class ArticleAdmin(admin.ModelAdmin):
    """Changes articles listing on admin panel."""
    model = Article
    list_display = ['title', 'get_outlet', 'date']

    def get_outlet(self, obj):
        """Shows outlet's name instead of its ID."""
        return obj.outlet.name
    get_outlet.admin_order_field = 'outlet'  #Allows column order sorting
    get_outlet.short_description = 'Outlet'  #Renames column head


admin.site.register(Author)
admin.site.register(Outlet, OutletAdmin)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
