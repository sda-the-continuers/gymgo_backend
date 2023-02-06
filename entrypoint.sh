#!/bin/sh

pwd
python --version
python manage.py migrate --no-input
python manage.py collectstatic --no-input

uwsgi --http :8000 --module gymtime_backend.wsgi