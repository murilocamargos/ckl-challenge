from rest_framework import serializers
from .models import Author, Outlet, Category, Article

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Author
        fields = ('id', 'name', 'slug', 'outlet', 'profile', 'twitter',
            'linkedin', 'facebook', 'website', 'avatar', 'about',
            'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class OutletSerializer(serializers.ModelSerializer):
    """Serializer to map the Outlet instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Outlet
        fields = ('id', 'name', 'slug', 'website', 'feed_url', 'description',
            'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class CategorySerializer(serializers.ModelSerializer):
    """Serializer to map the Category instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Category
        fields = ('id', 'name', 'slug', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to map the Article instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Article
        fields = ('id', 'title', 'date', 'url', 'thumb', 'content', 'author',
            'outlet', 'categories', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')