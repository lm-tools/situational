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
        az = Adzuna()
        adzuna_locations = az.locations_for_postcode(postcode)
        location, _ = models.JobLocation.objects.get_or_create(
            adzuna_locations=','.join(adzuna_locations),
        )
        report = models.JobDiscoveryReport.objects.create(
            location=location,
            postcode=postcode,
        )
        url = reverse('job_discovery:suggestion', kwargs={'guid': report.guid})
        return http.HttpResponseRedirect(url)


class SuggestionView(FormView):
    template_name = "job_discovery/suggestion.html"
    form_class = forms.SuggestionForm

    def dispatch(self, *args, **kwargs):
        self.report = models.JobDiscoveryReport.objects.get(pk=kwargs['guid'])
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.suggested_job = self.report.get_suggestion()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.suggested_job = models.Job.objects.get(pk=request.POST["job_id"])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        response = form.cleaned_data["response"]
        self.report.add_reaction(self.suggested_job, response)
        url = reverse('job_discovery:suggestion',
                      kwargs={'guid': self.report.guid})
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        context["job"] = self.suggested_job
        context["guid"] = self.report.pk
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['job_id'] = self.suggested_job.id
        return initial


class ReportView(TemplateView):
    template_name = "job_discovery/report.html"

    def get_context_data(self, **kwargs):
        context = kwargs
        report = models.JobDiscoveryReport.objects.get(pk=self.kwargs['guid'])
        context["jobs"] = report.liked_jobs
        return context
