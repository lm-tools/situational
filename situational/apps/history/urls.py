from django.conf.urls import patterns, url

from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url(r'form',
        TemplateView.as_view(template_name='history/form.html'),
        name="form")
)
