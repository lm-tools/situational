from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View

from . import forms
from . import models


class StartView(FormView):
    """
    Render PostcodeForm and redirect to ReportView when the form is valid.
    """

    template_name = "travel_report/start.html"
    form_class = forms.PostcodeForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode'].upper().replace(' ', '')
        url = reverse('report:show', kwargs={'postcode': postcode})
        return http.HttpResponseRedirect(url)


class ShowView(TemplateView):
    def get(self, request, *args, **kwargs):
        self.report, _created = models.TravelReport.objects.get_or_create(
            postcode=kwargs['postcode']
        )

        if self.report.is_populated:
            status_code = 200
            self.template_name = "travel_report/show.html"
        else:
            self.report.populate_async()
            status_code = 202
            self.template_name = "travel_report/pending.html"

        response = super().get(request, *args, **kwargs)
        response.status_code = status_code

        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        context['report'] = self.report
        return context


class PDFView(View):
    def get(self, request, *args, **kwargs):
        postcode = kwargs['postcode']
        report = get_object_or_404(models.TravelReport, postcode=postcode)
        response = http.HttpResponse(report.to_pdf(), 'application/pdf')
        response['Content-Disposition'] = \
            "filename={}-report.pdf".format(postcode)
        return response


class SendView(TemplateView):
    template_name = 'travel_report/send.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        postcode = kwargs['postcode']
        report = get_object_or_404(models.TravelReport, postcode=postcode)
        report.send_to(email)
        return super().get(self, request, *args, **kwargs)


class PopulatedResultFieldsView(View):
    def get(self, request, *args, **kwargs):
        try:
            report = models.TravelReport.objects.get(
                postcode=kwargs['postcode']
            )
            return http.JsonResponse(
                report.populated_result_fields,
                safe=False
            )
        except models.TravelReport.DoesNotExist:
            return http.HttpResponseNotFound()
