from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Author
        fields = ('id', 'name', 'slug', 'outlet', 'profile', 'twitter',
            'linkedin', 'facebook', 'website', 'avatar', 'about',
            'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')