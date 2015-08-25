from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'details$', views.HistoryDetailsView.as_view(), name="details"),
    url(r'report$', views.HistoryReportView.as_view(), name="report"),
    url(r'report\.pdf', views.PDFView.as_view(), name="pdf"),
    url(r'clear_session', views.ClearSessionView.as_view(),
        name="clear_session"),
    url(r'^$', views.StartView.as_view(),
        name="start"),
    url(r'send$', views.SendView.as_view(),
        name="send"),

]
