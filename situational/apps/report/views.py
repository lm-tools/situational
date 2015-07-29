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
        self.report, _created = models.Report.objects.get_or_create(
            postcode=kwargs['postcode']
        )

        if self.report.is_populated:
            status_code = 200
            self.template_name = "report/report_view.html"
        else:
            self.report.populate_async()
            status_code = 202
            self.template_name = "report/report_pending.html"

        response = super().get(request, *args, **kwargs)
        response.status_code = status_code

        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        context['report'] = self.report
        return context
