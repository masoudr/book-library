from time import sleep

from django.conf import settings
from django.test import TestCase
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from core.documents.book import BookDocument
from core.models import Author, Book


# Create Book URL
SEARCH_BOOK_URL = reverse('core:booksearch-list')


class TestBookDocument(TestCase):
    """Test BookDocument with ES"""

    def create_books(self):
        """Create Sample Books for authors"""
        for author in self.authors.values():
            # create author model
            _author = Author.objects.create(
                name=author['name'],
                email=author['email']
            )

            # create some books
            for book in author['books']:
                Book.objects.create(
                    author=_author,
                    name=book
                )

    def setUp(self):
        # wait for ES to start
        call_command('wait_for_es')
        # sample authors
        self.authors = {
            'author1': {
                "name": "Author1",
                "email": "Author1@test.com",
                "books": ["A1_B1", "A1_B2", "A1_B3", "A1_B4", "A1_B5", "A1_B6", "A1_B7"]
            },
            "author2": {
                "name": "Author2",
                "email": "Author2@test.com",
                "books": ["A2_B1", "A2_B2", "A2_B3", "A2_B4", "A2_B5", "A2_B6", "A2_B7"]
            }
        }
        self.create_books()

    def test_book_document_search_query(self):
        """Test ElasticSearch Query"""
        BookDocument.init()
        client = Elasticsearch(settings.ELASTICSEARCH_DSL['default']['hosts'])

        for author in self.authors.values():
            for book in author['books']:
                search = Search(using=client)
                search = search.query("match", name=book)
                self.assertTrue(search.count() > 0)
                result = search.execute(ignore_cache=True)
                res = result[0].to_dict()
                self.assertEqual(res['name'], book)

    def testtest_book_document_search_view(self):
        """Test ElasticSearch Search by making request to ViewSet"""
        for author in self.authors.values():
            for book in author['books']:
                data = {
                    'search': book,
                }
                res = self.client.get(
                    SEARCH_BOOK_URL,
                    data=data
                )
                self.assertEqual(res.status_code, status.HTTP_200_OK)
                self.assertEqual(res.data[0]['name'], book)
