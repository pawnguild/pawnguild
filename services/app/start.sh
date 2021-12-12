#!/bin/bash

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Creating migration files...'
python manage.py makemigrations

echo 'Migrating database...'
python manage.py migrate

echo 'Booting up server'
python manage.py runserver 0.0.0.0:8000