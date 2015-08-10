from django.conf.urls import patterns, url

from history import views

urlpatterns = patterns(
    '',
    url(r'form', views.HistoryForm.as_view(),
        name="form")
)
