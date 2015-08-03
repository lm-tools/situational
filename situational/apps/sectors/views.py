import requests

from django.views.generic import FormView
from django.views.generic import TemplateView

from .forms import SectorForm
from .helpers import LMIForAllClient


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
        return context


class SOCCodesView(TemplateView):
    template_name = "sectors/soc_codes.html"

    def get_context_data(self, **kwargs):
        context = kwargs
        soc_code_data = {}
        for soc_code in self.request.GET.keys():
            lmi_client = LMIForAllClient()
            soc_code_data[soc_code] = {
                'pay': lmi_client.pay(soc_code),
                'hours_worked': lmi_client.hours_worked(soc_code),
                'info': lmi_client.soc_code_info(soc_code)
            }

        context['soc_code_data'] = soc_code_data
        return context
