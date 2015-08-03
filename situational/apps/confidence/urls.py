from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',

    url(r'^new$',
        views.NewConfidenceReport.as_view(),
        name='new'),

    url(r'^$',
        views.ConfidenceReport.as_view(),
        name='show'),
)
