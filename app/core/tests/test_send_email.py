from django.test import TestCase
from django.core import mail

from core.models import Author, Book
from core.tasks import send_mail_to_authors


class SendMailCheck(TestCase):
    """
    Check Emails are sent successfully
    """

    def create_books(self):
        """
        Create Sample Books for authors
        """
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
        self.last_books_count = 5
        self.create_books()
        send_mail_to_authors()

    def test_send_email(self):
        """Test Send Email to authors"""
        author_length = Author.objects.all().count()

        # check length of outbox
        self.assertEqual(len(mail.outbox), author_length)
        # check each mail
        for outbox, author in zip(mail.outbox, self.authors.values()):
            author_name = author['name']
            last_books_as_str = ", ".join(
                author['books'][-self.last_books_count:])
            self.assertEqual(outbox.subject, 'Book Mail List')
            self.assertEqual(outbox.from_email, 'BookLibraryEmail@test.com')
            self.assertEqual(outbox.to, [author['email']])
            self.assertEqual(
                outbox.body, f'Dear {author_name}\nHere is your last {self.last_books_count} books: {last_books_as_str}')
