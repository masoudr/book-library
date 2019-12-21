from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from core.models import Author, Book
from core.documents.book import BookDocument


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


class BookDocumentSerializer(DocumentSerializer):
    """Serializer for Book serializer"""
    class Meta:
        document = BookDocument
        fields = ('author', 'name', 'created_on')
