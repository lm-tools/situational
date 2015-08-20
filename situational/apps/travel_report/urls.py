from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    '',

    url(r'(?P<postcode>[a-zA-Z0-9\s]+)/populated_result_fields.json$',
        views.PopulatedResultFieldsView.as_view(),
        name="populated_result_fields"),

    url(r'(?P<postcode>[a-zA-Z0-9\s]+)/send$',
        views.SendView.as_view(),
        name="send"),

    url(r'(?P<postcode>[a-zA-Z0-9\s]+).pdf$',
        views.PDFView.as_view(),
        name="pdf"),

    url(r'(?P<postcode>[a-zA-Z0-9\s]+)$',
        views.ShowView.as_view(),
        name="show"),

    url(r'^$',
        views.StartView.as_view(),
        name="start"),
)
