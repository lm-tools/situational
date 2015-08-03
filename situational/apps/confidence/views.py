from django.views.generic import FormView
from django.views.generic import TemplateView

from . import forms


class NewConfidenceReport(FormView):
    template_name = 'confidence/new.html'
    form_class = forms.ConfidenceReportForm


class ConfidenceReport(TemplateView):
    template_name = 'confidence/show.html'

    def get_context_data(self, **kwargs):
        context = kwargs
        q = self.request.GET
        context['success_confidence'] = q.get('success_confidence')
        context['search_confidence'] = q.get('search_confidence')
        return context
