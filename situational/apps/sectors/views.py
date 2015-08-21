import requests

from django import http
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View
from django.shortcuts import get_object_or_404

from .forms import SectorForm

from . import models


class SectorStartView(TemplateView):
    template_name = 'sectors/sector_start.html'


class SectorFromView(FormView):
    form_class = SectorForm
    template_name = 'sectors/sector_form.html'


class JobDescriptionsView(TemplateView):
    template_name = "sectors/job_descriptions.html"

    def lookup_from_lmi(self, keyword):
        BASE_URL = "http://api.lmiforall.org.uk/api/v1/soc/search"
        return requests.get(BASE_URL, params={'q': keyword}).json()

    def get_context_data(self, **kwargs):
        context = kwargs
        all_results = {}
        for key, value in self.request.GET.items():
            if key.startswith('sector_'):
                results = self.lookup_from_lmi(value)[:3]
                for result in results:
                    all_results[result['soc']] = result
        context['results'] = all_results
        context['postcode'] = self.request.GET['postcode'].strip()
        return context


class SOCCodesView(TemplateView):
    template_name = "sectors/report.html"

    def post(self, request, *args, **kwargs):
        postcode = self.request.POST['postcode']
        soc_codes = []
        for soc_code in self.request.POST.keys():
            if soc_code.startswith('soc_'):
                soc_code = soc_code[4:]
                soc_codes.append(soc_code)

        url_args = {'postcode': postcode, 'soc_codes': ",".join(soc_codes)}
        url = reverse('sectors:report', kwargs=url_args)
        return http.HttpResponseRedirect(url)


class ReportView(TemplateView):

    def get(self, request, *args, **kwargs):
        self.report, _created = models.SectorsReport.objects.get_or_create(
            postcode=kwargs['postcode'],
            soc_codes=kwargs['soc_codes']
        )

        if self.report.is_populated:
            status_code = 200
            self.template_name = "sectors/report.html"
        else:
            self.report.populate_async()
            status_code = 202
            self.template_name = "sectors/report_pending.html"

        response = super().get(request, *args, **kwargs)
        response.status_code = status_code

        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        context['report'] = self.report
        return context


class PopulatedResultFieldsView(View):
    def get(self, request, *args, **kwargs):
        try:
            report = models.SectorsReport.objects.get(
                postcode=kwargs['postcode'],
                soc_codes=kwargs['soc_codes']
            )
            return http.JsonResponse(
                report.populated_result_fields,
                safe=False
            )
        except models.SectorsReport.DoesNotExist:
            return http.HttpResponseNotFound()


class PDFView(View):
    def get(self, request, *args, **kwargs):
        postcode = kwargs['postcode']
        soc_codes = kwargs['soc_codes']
        report = get_object_or_404(
            models.SectorsReport,
            postcode=postcode,
            soc_codes=soc_codes
        )
        response = http.HttpResponse(report.to_pdf(), 'application/pdf')
        response['Content-Disposition'] = "filename=sectors-report.pdf"
        return response


class SendReportView(TemplateView):
    template_name = 'sectors/send_report.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        postcode = kwargs['postcode']
        soc_codes = kwargs['soc_codes']
        report = get_object_or_404(
            models.SectorsReport,
            postcode=postcode,
            soc_codes=soc_codes
        )
        report.send_to(email)
        return super().get(self, request, *args, **kwargs)
