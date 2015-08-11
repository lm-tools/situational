from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View
from history import forms


class HistoryDetailsView(FormView):
    """
    Render HistoryDetailsView and redirect to HistoryReportView when
    the form has been completed 3 times
    """

    template_name = "history/details.html"
    form_class = forms.HistoryDetailsForm

    def form_valid(self, form):
        url = reverse('history:report')
        return http.HttpResponseRedirect(url)


class HistoryReportView(TemplateView):
    def get(self, request, *args, **kwargs):
        self.template_name = "history/report.html"
        response = super().get(request, *args, **kwargs)
        return response
