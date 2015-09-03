from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.StartView.as_view(), name="start"),
    url(r'suggestion/(?P<guid>.+)/$',
        views.SuggestionView.as_view(), name="suggestion"),
    url(r'report/(?P<guid>.+)/$',
        views.ReportView.as_view(), name="report"),
    url(r'report/(?P<guid>.+)/send$', views.SendView.as_view(),
        name="send"),
    url(r'report/(?P<guid>.+).pdf$', views.PDFView.as_view(), name="pdf"),
]
