#!/bin/bash

set -e

echo "Collecting static assets..."
python manage.py collectstatic --noinput --ignore admin

echo "Running tests..."
python manage.py test --noinput

echo "Running flake8..."
flake8 .
