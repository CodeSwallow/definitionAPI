#!/bin/sh

 python manage.py migrate --noinput
# python manage.py collectstatic --no-input
 gunicorn definitionAPI.wsgi:application --bind 127.0.0.1:8000

exec "$@"