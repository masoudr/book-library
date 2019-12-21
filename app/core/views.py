from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters

from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FacetedSearchFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    PostFilterFilteringFilterBackend,
    CompoundSearchFilterBackend,
)

from core import models, serializers
from core.documents.book import BookDocument


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
    search_fields = ('author__name', 'name', 'created_on')


class BookDocumentViewSet(BaseDocumentViewSet):
    """Book Model for ES view"""
    document = BookDocument
    serializer_class = serializers.BookDocumentSerializer
    lookup_field = 'name'
    filter_backends = [
        FilteringFilterBackend,
        PostFilterFilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        CompoundSearchFilterBackend,
        FacetedSearchFilterBackend,
    ]

    # Define search fields
    search_fields = (
        'author.name',
        'name',
    )

    # Define filter fields
    filter_fields = {
        'name': 'name',
        'created_on': 'created_on',
    }

    # Define ordering fields
    ordering_fields = {
        'name': 'name',
        'created_on': 'created_on',
    }

    # Specify default ordering
    ordering = ('created_on',)

    faceted_search_fields = {
        'name': 'name',
    }

    post_filter_fields = {
        'name_pf': 'name',
        'created_on_pf': 'created_on'
    }
