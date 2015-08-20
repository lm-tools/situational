from django.conf.urls import url

from sectors import views

urlpatterns = [
    url(r'^$',
        views.SectorStartView.as_view(), name="sector_start"),
    url(r'^start$',
        views.SectorFromView.as_view(), name="sector_form"),
    url(r'job_descriptions', views.JobDescriptionsView.as_view(),
        name="job_descriptions"),
    url(r'soc_codes', views.SOCCodesView.as_view(),
        name="soc_code_info"),
]
