from django import http
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
        return kwargs

    def done(self, form_list, form_dict, **kwargs):
        sector_form = form_dict['sector_form']
        postcode = sector_form.cleaned_data['postcode']
        description_form = form_dict['job_descriptions_form']
        soc_codes = [k for k, v in description_form.cleaned_data.items() if v]
        soc_codes_string = ','.join(soc_codes)
        report, _created = models.SectorsReport.objects.get_or_create(
            postcode=postcode,
            soc_codes=soc_codes_string
        )
        url = reverse("sectors:report", kwargs={'report_id': report.pk})
        return HttpResponseRedirect(url)


class ReportView(TemplateView):

    def get(self, request, *args, **kwargs):
        self.report = get_object_or_404(
            models.SectorsReport,
            pk=int(kwargs['report_id'])
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
        report = get_object_or_404(
            models.SectorsReport,
            pk=int(kwargs['report_id'])
        )
        return http.JsonResponse(
            report.populated_result_fields,
            safe=False
        )


class PDFView(View):
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(
            models.SectorsReport,
            pk=int(kwargs['report_id'])
        )
        response = http.HttpResponse(report.to_pdf(), 'application/pdf')
        response['Content-Disposition'] = "filename=sectors-report.pdf"
        return response


class SendReportView(TemplateView):
    template_name = 'sectors/send_report.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        report = get_object_or_404(
            models.SectorsReport,
            pk=int(kwargs['report_id'])
        )
        report.send_to(email)
        return super().get(self, request, *args, **kwargs)
