from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'thank_you$', views.ThankYouView.as_view(), name="thank_you"),
    url(r'^$', views.HomePageView.as_view(), name="home"),
    url(r'^manifest.json$', views.ManifestView.as_view(), name="manifest"),

]
