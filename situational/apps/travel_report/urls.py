from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<postcode>[a-zA-Z0-9\s]+)/is_populated.json$',
        views.IsPopulatedView.as_view(),
        name="is_populated"),

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
]
