from .base import *


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Sym Roe', 'lmtools@talusdesign.co.uk'),
)

MANAGERS = ADMINS


import dj_database_url
DATABASES['default'] =  dj_database_url.config()

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
