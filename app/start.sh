#!/bin/bash

# waiting for MySQL db
python manage.py wait_for_db
# waiting for Elastic Search
python manage.py wait_for_es
# migrate DB
python manage.py migrate
# Rebuild Index for Elastic Search
yes | python manage.py search_index --rebuild
# Start Celery
/usr/local/bin/celery -A app worker --beat --loglevel=info &
# Start Server
python manage.py runserver 0.0.0.0:8000
