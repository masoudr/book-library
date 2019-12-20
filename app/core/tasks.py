from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from django.core.mail import send_mail
from core.models import Author, Book


# number of last books that needed to be sent via email
LAST_BOOKS_COUNT = 5


@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    print("***Hello from some_task***")


def send_mail_to_authors():
    """Send Book names to each Author"""
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
