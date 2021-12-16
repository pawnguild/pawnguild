#!/bin/bash

echo 'Collecting static files...'
python manage.py collectstatic --no-input

echo 'Creating migration files...'
python manage.py makemigrations

echo 'Migrating database...'
python manage.py migrate

echo 'Running tests...'
python manage.py test --no-input