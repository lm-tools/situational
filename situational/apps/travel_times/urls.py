from django.conf.urls import patterns, include, url

from travel_times import views

urlpatterns = [
    url(
        r'postcode/(?P<postcode>[a-zA-Z0-9\s]+)/image',
        views.MapView.as_view(), name="map",
    ),
]
