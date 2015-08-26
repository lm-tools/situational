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


import random
class JobSuggester():
    def __init__(self, job_pool):
        self.job_pool = job_pool

    def suggest_me_a_job(self, profile):
        return job_pool.sample(exclude=profile.all_job_ids)


class JobPool():
    def __init__(self, constraints):
        self.constraints = constraints


class SuggestionView(FormView):
    template_name = "job_discovery/suggestion.html"
    form_class = forms.SuggestionForm

    def get_context_data(self, **kwargs):
        context = kwargs
        # start a suggestion engine thing based on report
        # job_pool = job_pool.new(report.input_parameters)
        # job_pool.populate()
        # job = suggestion_engine.new(job_pool).suggest_me_a_job(report.output_so_far)
        context["job"] = {
            "job_id": "fasdhjasfdhkj",
            # the actual job should go there
        }
        return context

    def form_valid(self, form):
        report = {} # get the report from the guid
        job_id = "bla"
        liked_status= "much liked, such thumbs up"
        # put that job_id and liked status in the report and save
        url = reverse('job_discovery:suggestion', kwargs={'guid': guid})
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
