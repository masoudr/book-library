import time
import urllib3
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """
    Django command to pause executaion until ElasticSeach container is available
    """

    def handle(self, *args, **options):
        self.stdout.write('waiting for ES...')
        db_conn = None
        es_url = 'http://' + settings.ELASTICSEARCH_DSL['default']['hosts']
        while not db_conn:
            try:
                http = urllib3.PoolManager()
                res = http.request('GET', es_url)
                if res.status == 200:
                    db_conn = True
            except Exception:
                self.stdout.write('ES unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('ES available!'))
