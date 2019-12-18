from rest_framework import serializers

from core.models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    """Author Serializer"""

    class Meta:
        model = Author
        fields = ('name', 'email')
        read_only_fields = ('id',)


class BookSerializer(serializers.ModelSerializer):
    """Book Seiralizer"""

    class Meta:
        model = Book
        fields = ('author', 'name', 'created_on')
        read_only_fields = ('id', 'created_on')
