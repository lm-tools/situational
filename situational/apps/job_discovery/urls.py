from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'start$', views.StartView.as_view(), name="start"),
    url(r'suggestion/(?P<guid>.+)/$',
        views.SuggestionView.as_view(), name="suggestion"),
    url(r'report/(?P<guid>.+)/$',
        views.ReportView.as_view(), name="report"),
]
