from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from formtools.wizard.views import NamedUrlCookieWizardView


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
