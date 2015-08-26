from .base import *

# Sets CELERY_ALWAYS_EAGER=True, making celery tasks block.
# This makes testing much easier.
# http://docs.celeryproject.org/en/2.5/django/unit-testing.html
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

if ADZUNA_APP_ID is None:
    ADZUNA_APP_ID = "dummay_adzuna_app_id"

if ADZUNA_APP_KEY is None:
    ADZUNA_APP_KEY = "dummay_adzuna_app_key"

BASICAUTH_DISABLED = True
LOGGING['root']['level'] = 'WARNING'
SECRET_KEY = 'not_a_secret'
