from django import http
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, View

from . import forms, models, pdf
from home_page import forms as shared_forms
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
        context["job_pool_location"] = self.report.location.adzuna_locations
        context["report"] = self.report
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['job_id'] = self.suggested_job.id
        return initial


class ReportView(FormView):
    template_name = "job_discovery/report.html"
    form_class = shared_forms.EmailForm
    success_url = "#success"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = kwargs
        report = models.JobDiscoveryReport.objects.get(pk=self.kwargs['guid'])
        context["jobs"] = report.liked_jobs
        context["job_pool_location"] = report.location.adzuna_locations
        context["guid"] = report.guid
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        report = models.JobDiscoveryReport.objects.get(pk=self.kwargs['guid'])
        report.send_to(email)
        notice = "Your report has been sent to " + email
        messages.success(self.request, notice)
        return super(ReportView, self).form_valid(form)


class PDFView(View):
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(
            models.JobDiscoveryReport,
            pk=kwargs['guid']
        )
        pdf_contents = pdf.render(report)
        response = http.HttpResponse(pdf_contents, 'application/pdf')
        response['Content-Disposition'] = "filename=job-discovery-report.pdf"
        return response
