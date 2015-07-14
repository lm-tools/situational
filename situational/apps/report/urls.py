from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'', views.PostcodeLookupView.as_view(), name="postcode_lookup_view"),
    url(r'report/(?P<postcode>[a-zA-Z0-9\s]+)', views.ReportView.as_view(), name="report_view"),
)
