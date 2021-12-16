#!/bin/bash

# echo 'Collecting static files...'
# python manage.py collectstatic --no-input

# echo 'Creating migration files...'
# python manage.py makemigrations

# echo 'Migrating database...'
# python manage.py migrate

echo 'Creating superuser...'
python manage.py createsuperuser --noinput

echo 'Booting up server'
gunicorn config.wsgi:application --bind 0.0.0.0:8000

