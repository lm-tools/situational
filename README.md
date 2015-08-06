## Running

Depends on Python >= 3.4, Sass 3.2.19, Redis >= 3.0

Install python dependancies for your environment (local, production, etc):

> pip install -r requirements/[env].txt

For async task running, run a celery worker:

> ./manage.py celery -A situational worker -l debug

To run the dev server

> ./manage.py runserver

Or use `foreman` to run as heroku would:

> foreman start
