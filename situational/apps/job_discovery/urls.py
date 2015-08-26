from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.StartView.as_view(), name="start"),
    url(r'suggestion/(?P<guid>.+)/$',
        views.SuggestionView.as_view(), name="suggestion"),
    url(r'job_cards$', views.JobCardsView.as_view(), name="job_cards"),
]
