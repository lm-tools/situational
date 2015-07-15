from django.conf.urls import patterns, url

from report import views

urlpatterns = patterns(
    '',
    url(r'report/(?P<postcode>[a-zA-Z0-9\s]+)',
        views.ReportView.as_view(), name="report_view"),
    url(r'', views.PostcodeLookupView.as_view(),
        name="postcode_lookup_view"),
)
