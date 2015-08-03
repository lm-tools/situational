from django.views.generic import FormView
from django.views.generic import TemplateView

from . import forms


class NewConfidenceReport(FormView):
    template_name = 'confidence/new.html'
    form_class = forms.ConfidenceReportForm


class ConfidenceReport(TemplateView):
    template_name = 'confidence/show.html'
