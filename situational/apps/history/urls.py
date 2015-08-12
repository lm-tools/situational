from django.conf.urls import patterns, url

from history import views

urlpatterns = patterns(
    '',
    url(r'details', views.HistoryDetailsView.as_view(),
        name="details"),
    url(r'report', views.HistoryReportView.as_view(),
        name="report")
)
