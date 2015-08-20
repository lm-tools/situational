from django.conf.urls import url

from . import views

postcode = "(?P<postcode>[a-zA-Z0-9\s]+)"
soc_codes = "(?P<soc_codes>[-\w\s]+(?:,[-\w\s]*)*)"

urlpatterns = [
    url(r'^$',
        views.SectorStartView.as_view(), name="sector_start"),

    url(r'^start$',
        views.SectorFromView.as_view(), name="sector_form"),

    url(r'job_descriptions', views.JobDescriptionsView.as_view(),
        name="job_descriptions"),

    url(r'soc_codes$', views.SOCCodesView.as_view(),
        name="soc_code_info"),

    url(r'soc_codes/' + postcode + '/' + soc_codes + '$',
        views.ReportView.as_view(),
        name="report"),

    url(r'soc_codes/' + postcode + '/' + soc_codes + '/send$',
        views.SendReportView.as_view(),
        name="send_report"),
]
