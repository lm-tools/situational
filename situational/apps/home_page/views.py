from django import http
from django.apps import apps
from django.conf import settings
from django.core.urlresolvers import reverse
from django.templatetags.static import static
from django.views.generic import FormView, TemplateView

from . import forms, tasks


class HomePageView(FormView):
    template_name = "home_page/home.html"
    form_class = forms.FeedbackForm

    def form_valid(self, form):
        tasks.send_feedback.delay(
            form.data['name'],
            form.data['email'],
            form.data['subject'],
            form.data['message']
        )
        url = reverse('home_page:thank_you')
        return http.HttpResponseRedirect(url)


class ThankYouView(TemplateView):
    template_name = "home_page/thank_you.html"


class ManifestView(TemplateView):
    template_name = "home_page/manifest.json"
    content_type = "application/json"

    def get_context_data(self, **kwargs):
        default_app_name = settings.DEFAULT_MANIFEST_APP_NAME
        app_name = self.request.GET.get('app', default_app_name)
        app_config = apps.get_app_config(app_name)
        if not hasattr(app_config, 'manifest') or not app_config.manifest:
            app_name = default_app_name
            app_config = app_config = apps.get_app_config('home_page')

        context = kwargs
        context['icon_url'] = static(app_config.icon_url)
        context['title'] = app_config.verbose_name
        context['start_url'] = reverse("{0}:{1}".format(
            app_name,
            app_config.start_url_name
        ))
        return kwargs
