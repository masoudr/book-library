from __future__ import absolute_import, unicode_literals
from celery.decorators import periodic_task
from celery.task.schedules import crontab
import logging
from django.core.mail import send_mail
from django.db import transaction

from core.models import Author, Book

logger = logging.getLogger()

# number of last books that needed to be sent via email
LAST_BOOKS_COUNT = 5


def send_mail_to_authors_helper():
    """Helper function for send_mail_to_authors"""
    for author in Author.objects.all():
        # retrieve last 5 book names
        last_books = Book.objects.filter(author=author).values_list(
            'name', flat=True).order_by('-id')[:LAST_BOOKS_COUNT][::-1]
        last_books_as_str = ", ".join(last_books)
        send_mail('Book Mail List',
                  f'Dear {author.name}\nHere is your last {LAST_BOOKS_COUNT} books: {last_books_as_str}',
                  'BookLibraryEmail@test.com',
                  [author.email],
                  fail_silently=False,)

        # send a log to MongoDB
        logger.info(
            f'An email with last {LAST_BOOKS_COUNT} books sent to {author.name}!')


@periodic_task(run_every=(crontab(hour=17, minute=0, day_of_week=1)), name="send_mail_to_authors", ignore_result=True)
def send_mail_to_authors():
    """Send Email with book names to each author every Monday at 17:00"""
    transaction.on_commit(send_mail_to_authors_helper)
