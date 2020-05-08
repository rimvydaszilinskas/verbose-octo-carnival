#!/usr/bin/env bash

sleep 5
cd /code

python manage.py migrate

gunicorn core.wsgi:application --bind 0.0.0.0:8001 --workers 3
