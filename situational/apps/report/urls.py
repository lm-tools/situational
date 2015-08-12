from django.conf.urls import patterns, url

from report import views

urlpatterns = patterns(
    '',

    url(r'report/(?P<postcode>[a-zA-Z0-9\s]+)/populated_result_fields.json$',
        views.ReportPopulatedResultFieldsView.as_view(),
        name="report_populated_result_fields"),

    url(r'report/(?P<postcode>[a-zA-Z0-9\s]+)/send$',
        views.ReportSendView.as_view(),
        name="report_send"),

    url(r'report/(?P<postcode>[a-zA-Z0-9\s]+).pdf$',
        views.ReportPDFView.as_view(), name="report_pdf"),

    url(r'report/(?P<postcode>[a-zA-Z0-9\s]+)$',
        views.ReportView.as_view(), name="report_view"),

    url(r'^$', views.PostcodeLookupView.as_view(),
        name="postcode_lookup_view"),
)
