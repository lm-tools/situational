from django import http
from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView

from . import forms, models
from .adzuna import Adzuna


class StartView(FormView):
    template_name = "job_discovery/start.html"
    form_class = forms.PostcodeForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode'].upper().replace(' ', '')
        report = models.JobDiscoveryReport.objects.create(
            postcode=postcode
        )
        url = reverse('job_discovery:suggestion', kwargs={'guid': report.guid})
        return http.HttpResponseRedirect(url)


class SuggestionView(FormView):
    template_name = "job_discovery/suggestion.html"
    form_class = forms.SuggestionForm

    def get_context_data(self, **kwargs):
        context = kwargs
        report = models.JobDiscoveryReport.objects.get(pk=self.kwargs['guid'])
        context["job"] = report.get_suggestion()
        return context

    def form_valid(self, form):
        report = models.JobDiscoveryReport.objects.get(pk=self.kwargs['guid'])
        job = models.Job.objects.get(pk=form.cleaned_data["job_id"])
        response = form.cleaned_data["response"]
        report.add_reaction(job, response)
        url = reverse('job_discovery:suggestion', kwargs={'guid': report.guid})
        return http.HttpResponseRedirect(url)


class ReportView(TemplateView):
    template_name = "job_discovery/report.html"

    def get_context_data(self, **kwargs):
        context = kwargs
        # get that report from the guid
        context["report"] = {}
        return context


class JobCardsView(TemplateView):
    template_name = "job_discovery/job_cards.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        az = Adzuna()
        context['jobs'] = az.jobs_at_location(
            'UK',
            'London',
            'Central London',
            50
        )
        return context
