import requests

from django.views.generic import TemplateView


class HistoryForm(TemplateView):
    template_name = 'history/form.html'
