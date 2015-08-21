# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'history/', include('history.urls', namespace='history')),
    url(r'quick_history/', include('history.urls', namespace='history')),
    url(r'sectors/', include('sectors.urls', namespace='sectors')),
    url(r'travel/', include('travel_report.urls', namespace='travel_report')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
