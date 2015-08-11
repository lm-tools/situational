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
        if 'forms' not in self.request.session:
            self.request.session['forms'] = []
        self.request.session['forms'] += [form.data]
        if len(self.request.session['forms']) < 3:
            url = reverse('history:details')
        else:
            url = reverse('history:report')
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs

        def remove_csrf_field(form_data):
            form_data.pop("csrfmiddlewaretoken", None)
            return form_data
        form_data = [
            remove_csrf_field(l) for l in self.request.session['forms']]
        context['report'] = form_data
        return context


class HistoryReportView(TemplateView):
    def get(self, request, *args, **kwargs):
        self.template_name = "history/report.html"
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = kwargs

        def remove_csrf_field(form_data):
            form_data.pop("csrfmiddlewaretoken", None)
            return form_data
        form_data = [
            remove_csrf_field(l) for l in self.request.session['forms']]
        context['report'] = form_data
        return context
