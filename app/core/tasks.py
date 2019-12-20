from __future__ import absolute_import, unicode_literals
from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab


@periodic_task(run_every=(crontab(minute='*/1')), name="some_task", ignore_result=True)
def some_task():
    print("***Hello from some_task***")
