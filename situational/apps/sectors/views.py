from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from formtools.wizard.views import NamedUrlCookieWizardView

from . import models


class SectorStartView(TemplateView):
    template_name = 'sectors/sector_start.html'


class SectorWizardView(NamedUrlCookieWizardView):
    TEMPLATES = {
        'sector_form': 'sectors/sector_form.html',
        'job_descriptions_form': 'sectors/job_descriptions.html',
        'soc_codes_form': 'sectors/soc_codes.html'
    }

    def get(self, *args, **kwargs):
        if 'restart' in self.request.GET:
            self.storage.reset()
            return HttpResponseRedirect(reverse('sectors:start'))
        return super().get(*args, **kwargs)

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):
        kwargs = {}
        if step == 'job_descriptions_form':
            sectors = self.get_cleaned_data_for_step('sector_form')['sector']
            kwargs['keywords'] = sectors

        if step == 'soc_codes_form':
            codes = self.get_cleaned_data_for_step('job_descriptions_form')
            kwargs['soc_codes'] = [k for k, v in codes.items() if v]
            kwargs['postcode'] = \
                self.get_cleaned_data_for_step('sector_form')['postcode']
        return kwargs


    def post(self, request, *args, **kwargs):
        postcode = self.request.POST['postcode']
        soc_codes = []
        for soc_code in self.request.POST.keys():
            if soc_code.startswith('soc_'):
                soc_code = soc_code[4:]
                soc_codes.append(soc_code)

        url_args = {
            'postcode': postcode,
            'soc_codes': ",".join(sorted(soc_codes))
        }
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
