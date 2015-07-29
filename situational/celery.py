import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'situational.settings')

from django.conf import settings

app = Celery('situational')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.update(
    BROKER_URL=os.environ.get('CELERY_BROKER_URL', settings.REDIS_URL),
    CELERY_RESULT_BACKEND=settings.REDIS_URL,
)