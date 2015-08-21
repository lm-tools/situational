from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'details', views.HistoryDetailsView.as_view(), name="details"),
    url(r'report', views.HistoryReportView.as_view(), name="report"),
    url(r'clear_session', views.ClearSessionView.as_view(),
        name="clear_session"),
    url(r'start', views.HistoryStartStructuredView.as_view(),
        name="start"),
]
