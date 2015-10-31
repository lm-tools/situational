# Situational

## Deploying

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/lm-tools/situational)

### Environment variables

#### All tools

* DEFAULT_FROM_EMAIL
* DJANGO_SECRET_KEY
* HTTP_PASSWORD
* HTTP_USERNAME
* GOOGLE_ANALYTICS_ID

#### Travel tool

* AWS_ACCESS_KEY_ID
* AWS_S3_HOST
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAME
* MAPUMENTAL_API_KEY
* ENABLE_MAPUMENTAL

#### Discovery tool

To signup for Adzuna, go to: https://developer.adzuna.com/signup.

* ADZUNA_APP_ID
* ADZUNA_APP_KEY

## Running

Depends on Python >= 3.4, Sass 3.2.19, Redis >= 3.0

Install python dependancies for your environment (local, production, etc):

> pip install -r requirements/[env].txt

Install asset pipeline dependancies:

> bundle install

For async task running, run a celery worker:

> ./manage.py celery -A situational worker -l debug

To run the dev server

> ./manage.py runserver

Or use `foreman` to run as heroku would:

> foreman start

## Faster asset compilation in development

[SASS](http://sass-lang.com/), while awesome, is (comparatively) slow. Compilation of scss assets takes ~1.5s.

To speed asset compilation up locally, replace sass with [sassc](https://github.com/sass/sassc) as follows:

1. install sassc (`brew install sassc`)
2. add the following to `situational/settings/local.py`:

```python
STATIC_PRECOMPILER_COMPILERS = (
    'static_precompiler.compilers.SCSS', {'executable': 'sassc'}),
)
```
