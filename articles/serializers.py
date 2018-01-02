from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from articles.models import Author, Outlet, Category, Article

class MyJSONRenderer(JSONRenderer):
    """Overloads default JSONRederer to force pretty print."""
    def get_indent(self, accepted_media_type, renderer_context):
        """Gives indentation size for pretty print JSON."""
        return renderer_context.get('indent', 4)



class AuthorSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Author
        fields = ('id', 'name', 'outlet', 'avatar', 'about', 'twitter',
            'facebook', 'linkedin', 'profile', 'website')


class OutletSerializer(serializers.ModelSerializer):
    """Serializer to map the Outlet instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Outlet
        fields = ('id', 'name', 'website', 'description')



class CategorySerializer(serializers.ModelSerializer):
    """Serializer to map the Category instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Category
        fields = ('id', 'name', 'slug')



class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to map the Article instance into JSON format."""

    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False,
    )

    authors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Author.objects.all(),
        required=False
    )

    outlet = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Outlet.objects.all()
    )

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Article
        fields = ('id', 'title', 'date', 'url', 'thumb', 'content', 'authors',\
            'outlet', 'categories')



class ArticleRetrieveSerializer(serializers.ModelSerializer):
    """
    This serializer is only for retrieving articles. We wanted to show the
    nested information of outlet, authors and categories along the article's.
    """

    categories = CategorySerializer(many=True)
    authors = AuthorSerializer(many=True)
    outlet = OutletSerializer(many=False)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Article
        fields = ('id', 'title', 'date', 'url', 'thumb', 'content', 'authors',\
            'outlet', 'categories')
