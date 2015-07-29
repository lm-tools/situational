#!/bin/bash

set -e

echo "Running tests..."
python manage.py test

echo "Running pep8..."
pep8 .
