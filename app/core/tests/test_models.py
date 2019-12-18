from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from core.models import Author, Book

# Create Author URL
CREATE_AUTHOR_URL = reverse('core:author-list')

# Create Book URL
CREATE_BOOK_URL = reverse('core:book-list')


def sample_user(email='test@test.com', password='testpass'):
    """Create a Sample User"""
    return get_user_model().objects.create_user(email, password)


class AuthorModelTests(TestCase):
    """Test Author Model"""

    def setUp(self):
        self.user = sample_user()

    def test_create_author(self):
        """Test Create Author"""
        payload = {
            'name': 'TestAuthor',
            'email': 'test@test.com'
        }
        res = self.client.post(CREATE_AUTHOR_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Author.objects.filter(**payload).exists())


class BookModelTests(TestCase):
    """Test Book Model"""

    def setUp(self):
        self.user = sample_user()

    def create_author(self):
        """Create Author Model"""
        author = {
            'name': 'TestAuthor',
            'email': 'test@test.com'
        }
        return Author.objects.create(**author)

    def test_create_book(self):
        """Test Create Book for Author"""
        author = self.create_author()
        payload = {
            'author': author.id,
            'name': 'SampleBook'
        }
        res = self.client.post(CREATE_BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(**payload).exists())
