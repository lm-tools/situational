from django import http
from django.core.urlresolvers import reverse
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
