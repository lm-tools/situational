#!/usr/bin/env bash

set -eo pipefail

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static assets..."
python manage.py collectstatic --noinput --ignore admin
