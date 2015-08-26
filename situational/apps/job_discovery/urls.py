from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'job_cards$', views.JobCardsView.as_view(), name="job_cards"),
]
