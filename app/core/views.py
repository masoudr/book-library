from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters

from core import models, serializers


class AuthorViewSet(viewsets.ModelViewSet):
    """Authro ViewSet"""
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.all()

    # add filters to viewset
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class BookViewSet(viewsets.ModelViewSet):
    """Book ViewSet"""
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()

    # add filters to viewset
    filter_backends = (filters.SearchFilter,)
    search_fields = ('author', 'name', 'created_on')
