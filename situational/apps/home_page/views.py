from django import http
from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView

from . import forms


class HomePageView(FormView):
    template_name = "home_page/home.html"
    form_class = forms.FeedbackForm

    def form_valid(self, form):
        # TODO: actually send the email...
        url = reverse('home_page:thank_you')
        return http.HttpResponseRedirect(url)


class ThankYouView(TemplateView):
    template_name = "home_page/thank_you.html"
