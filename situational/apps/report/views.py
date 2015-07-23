from django import http
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic import FormView

from report import helpers
from report import forms
from report import models


class PostcodeLookupView(FormView):
    """
    Render PostcodeForm and redirect to ReportView when the form is valid.
    """

    template_name = "report/postcode_view.html"
    form_class = forms.PostcodeForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode'].upper().replace(' ', '')
        url = reverse('report_view', kwargs={'postcode': postcode})
        return http.HttpResponseRedirect(url)


class ReportView(TemplateView):
    def get(self, request, *args, **kwargs):
        report = models.Report(kwargs['postcode'])

        if report.is_populated:
            status_code = 200
            self.template_name = "report/report_view.html"
        else:
            report.populate_async()
            status_code = 202
            self.template_name = "report/report_pending.html"

        response = super().get(request, *args, **kwargs)
        response.status_code = status_code

        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        context['location'] = helpers.geocode(context['postcode'])
        context['place_name'] = \
            helpers.place_name_from_location(**context['location'])
        context['top_categories'] = \
            helpers.top_categories_for_postcode(context['postcode'])
        context['top_companies'] = \
            helpers.top_companies_for_postcode(context['postcode'])
        context['latest_jobs'] = \
            helpers.latest_jobs_for_postcode(context['postcode'])
        return context
