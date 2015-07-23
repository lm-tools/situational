web: python manage.py migrate --noinput && gunicorn situational.wsgi --log-file -
celery: celery -A situational worker -l info
