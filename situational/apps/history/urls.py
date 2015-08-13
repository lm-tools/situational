from django.conf.urls import patterns, url

from history import views

urlpatterns = patterns(
    '',
    url(r'details', views.HistoryDetailsView.as_view(),
        name="details"),
    url(r'report', views.HistoryReportView.as_view(),
        name="report"),
    url(r'clear_session', views.ClearSessionView.as_view(),
        name="clear_session")
)
