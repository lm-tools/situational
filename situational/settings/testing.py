from .base import *

# Sets CELERY_ALWAYS_EAGER=True, making celery tasks block.
# This makes testing much easier.
# http://docs.celeryproject.org/en/2.5/django/unit-testing.html
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

LOGGING['root']['level'] = 'WARNING'
