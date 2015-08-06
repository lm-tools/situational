#!/bin/bash

set -e

echo "Collecting static assets..."
python manage.py collectstatic --noinput

echo "Running tests..."
python manage.py test --noinput

echo "Running pep8..."
pep8 .
