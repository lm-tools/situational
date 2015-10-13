from django import http
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import FormView
from django.views.generic import View

from . import forms
from . import models
from home_page import forms as shared_forms


class StartView(FormView):
    """
    Render PostcodeForm and redirect to ReportView when the form is valid.
    """

    template_name = "travel_report/start.html"
    form_class = forms.PostcodeForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode'].upper().replace(' ', '')
        url = reverse('travel_report:report', kwargs={'postcode': postcode})
        return http.HttpResponseRedirect(url)


class ReportView(FormView):
    template_name = "travel_report/report.html"
    form_class = shared_forms.EmailForm
    success_url = "#success"

    def get(self, request, *args, **kwargs):
        self.report, _created = models.TravelReport.objects.get_or_create(
            postcode=kwargs['postcode']
        )

        if self.report.is_populated:
            status_code = 200
            self.template_name = "travel_report/report.html"
        else:
            self.report.populate_async()
            status_code = 202
            self.template_name = "travel_report/pending.html"

        response = super().get(request, *args, **kwargs)
        response.status_code = status_code

        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        report = models.TravelReport.objects.get(
            postcode=self.kwargs['postcode']
        )
        context['report'] = report
        context['postcode'] = report.postcode
        return context

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        report = models.TravelReport.objects.get(
            postcode=self.kwargs['postcode']
        )
        report.send_to(email)
        notice = "Your report has been sent to " + email
        messages.success(self.request, notice)
        return super(ReportView, self).form_valid(form)


class PDFView(View):
    def get(self, request, *args, **kwargs):
        postcode = kwargs['postcode']
        report = get_object_or_404(models.TravelReport, postcode=postcode)
        response = http.HttpResponse(report.to_pdf(), 'application/pdf')
        response['Content-Disposition'] = \
            "filename={}-report.pdf".format(postcode)
        return response


class IsPopulatedView(View):
    def get(self, request, *args, **kwargs):
        try:
            report = models.TravelReport.objects.get(
                postcode=kwargs['postcode']
            )
            return http.JsonResponse(
                report.is_populated,
                safe=False
            )
        except models.TravelReport.DoesNotExist:
            return http.HttpResponseNotFound()
