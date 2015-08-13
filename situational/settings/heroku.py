import os

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sym Roe', 'lmtools@talusdesign.co.uk'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = ['.herokuapp.com']

# Redirect any non-HTTP request to HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Only allow sessions when serving the site over HTTPS
SESSION_COOKIE_SECURE = True

# Only send CSRF protection cookies when serving the site over HTTPS
CSRF_COOKIE_SECURE = True

# Use the X-Request=ID HTTP Header as the request ID
LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"

import dj_database_url
DATABASES['default'] = dj_database_url.config()
DATABASES['default']['ENGINE'] = 'django_postgrespool'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_HOST = os.environ['AWS_S3_HOST']

REDIS_URL = os.environ['REDISCLOUD_URL']

EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
EMAIL_USE_TLS = True
