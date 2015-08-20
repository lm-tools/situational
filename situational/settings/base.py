import sys
from os import environ
from os.path import join, abspath, dirname
from django.core.exceptions import ImproperlyConfigured


# PATH vars
def here(*x):
    return join(abspath(dirname(__file__)), *x)


PROJECT_ROOT = here("..")


def root(*x):
    return join(abspath(PROJECT_ROOT), *x)


sys.path.insert(0, root('apps'))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django_postgrespool',
        'NAME': 'situational',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = root('uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = root('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    root('assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Make this unique, and don't share it with anybody.
SECRET_KEY = environ.get('DJANGO_SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

BASICAUTH_USERNAME = environ.get('HTTP_USERNAME')
BASICAUTH_PASSWORD = environ.get('HTTP_PASSWORD')
if 'BASICAUTH_DISABLED' not in locals():
    BASICAUTH_DISABLED = environ.get('BASICAUTH_DISABLED') == 'True'


MIDDLEWARE_CLASSES = (
    'log_request_id.middleware.RequestIDMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'situational.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'situational.wsgi.application'

TEMPLATE_DIRS = (
    root('templates'),
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'storages',
    'djcelery',
    'pipeline',
)

PROJECT_APPS = (
    'basicauth',
    'history',
    'travel_report',
    'sectors',
    'template_to_pdf',
    'templated_email',
    'travel_times',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

INSTALLED_APPS += PROJECT_APPS

# Log on standard out. Doing something with the logs is left up to the parent
# process
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter',
        }
    },
    'formatters': {
        'standard': {
            'format': '[%(levelname)s] [%(request_id)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'console_with_request_id': {
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': environ.get('ROOT_LOG_LEVEL', 'INFO'),
    },
    'loggers': {
        'django': {
            'handlers': ['console_with_request_id'],
            'level': environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

# EMAILS
DEFAULT_FROM_EMAIL = environ.get('DEFAULT_FROM_EMAIL', 'webmaster@localhost')

# Jobs API
JOBS_API_BASE_URL = environ.get('JOBS_API_BASE_URL',
                                'https://lmt-jobs-api.herokuapp.com')

# MAPUMENTAL
MAPUMENTAL_API_KEY = environ.get('MAPUMENTAL_API_KEY')

BROKER_URL = environ.get('REDISTOGO_URL',
                         'redis://localhost:6379/0')

from travel_times import mapumental
if environ.get('ENABLE_MAPUMENTAL'):
    MAPUMENTAL_CLIENT = mapumental.Client
else:
    MAPUMENTAL_CLIENT = mapumental.FakeClient

# REDIS
REDIS_URL = environ.get('REDIS_URL', 'redis://')

# REPORT POPULATION
REPORT_POPULATION_TIMEOUT = int(
    environ.get('REPORT_POPULATION_TIMEOUT', 90000)
)

LMI_FOR_ALL_API_URL = environ.get(
    'LMI_FOR_ALL_API_URL',
    'http://api.lmiforall.org.uk/api/v1/'
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
)
PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'css/normalize.css',
            'css/foundation.css',
            'css/styles.scss',
            'css/timeline.scss'
        ),
        'output_filename': 'css/main.min.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}
PIPELINE_YUGLIFY_BINARY = root('..', 'node_modules', '.bin', 'yuglify')
PIPELINE_SASS_BINARY = root('..', 'bin', 'sass')

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass


# importing test settings file if necessary (TODO chould be done better)
if len(sys.argv) > 1 and 'test' in sys.argv[1]:
    from .testing import *

# This check is at the end of this so that it can be overridden by environment
# specific config
if BASICAUTH_DISABLED is False \
        and all((BASICAUTH_USERNAME, BASICAUTH_PASSWORD)) is False:
    raise ImproperlyConfigured("Please specify a HTTP username and password")

if not BASICAUTH_DISABLED:
    MIDDLEWARE_CLASSES = tuple(
        [
            'basicauth.basic_auth_middleware.BasicAuthMiddleware',
        ] + list(MIDDLEWARE_CLASSES)
    )
