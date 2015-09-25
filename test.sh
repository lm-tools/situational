#!/usr/bin/env bash

set -eo pipefail

echo "Running tests..."
python manage.py test --noinput

echo "Running flake8..."
flake8 .
