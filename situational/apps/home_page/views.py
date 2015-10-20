from django import http
from django.apps import apps
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.templatetags.static import static
from django.views.generic import FormView, TemplateView

from . import forms, tasks


def app_config_from_namespace(namespace):
    defaut_namespace = settings.DEFAULT_APP_NAMESPACE
    app_config = apps.get_app_config(namespace)
    if not hasattr(app_config, 'manifest') or not app_config.manifest:
        namespace = defaut_namespace
        app_config = apps.get_app_config('home_page')
    return namespace, app_config


def url_from_app_config(namespace, app_config):
    return reverse("{0}:{1}".format(
        namespace,
        app_config.start_url_name
    ))


class HomePageView(FormView):
    template_name = "home_page/home.html"
    form_class = forms.FeedbackForm

    def form_valid(self, form):
        tasks.send_feedback.delay(
            form.data['name'],
            form.data['email'],
            form.data['message'],
            dict(forms.TOOLS)[form.data['tool']],
            dict(forms.FEEDBACK_TYPES)[form.data['feedback_type']]
        )
        url = reverse('home_page:thank_you')
        return http.HttpResponseRedirect(url)

    def get_form_kwargs(self):
        kwargs = super(HomePageView, self).get_form_kwargs()
        print(self.request.GET)
        referring_url = self.request.GET.get('referring_url')
        kwargs['initial']['referring_url'] = referring_url
        tool = 'all'
        if referring_url:
            if referring_url.find("travel") != -1:
                tool = 'travel'
            elif referring_url.find("sectors") != -1:
                tool = 'sectors'
            elif referring_url.find("discovery") != -1:
                tool = 'discovery'
        kwargs['initial']['tool'] = tool
        return kwargs


class ThankYouView(TemplateView):
    template_name = "home_page/thank_you.html"


class ManifestView(TemplateView):
    template_name = "home_page/manifest.json"
    content_type = "application/json"

    def get_context_data(self, **kwargs):
        initial_namespace = self.request.GET.get('app')
        namespace, app_config = app_config_from_namespace(initial_namespace)

        context = kwargs
        context['icon_url'] = static(app_config.icon_url)
        context['title'] = app_config.verbose_name
        context['start_url'] = url_from_app_config(namespace, app_config)
        return kwargs


def server_error(request, template_name='500.html'):
    initial_namespace = request.resolver_match.namespace
    namespace, app_config = app_config_from_namespace(initial_namespace)
    start_url = url_from_app_config(namespace, app_config)

    context_instance = RequestContext(request)
    context_instance['start_url'] = start_url

    return render_to_response(
        template_name,
        context_instance=context_instance
    )
