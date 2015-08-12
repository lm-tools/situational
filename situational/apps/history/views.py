from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View
from history import forms


def get_form_data_from_session(session):
    form_data = session['forms']
    for form in form_data:
        form.pop("csrfmiddlewaretoken", None)
    return form_data


def format_history_entry(entry):
    description = ""
    if entry["description"][0]:
        description = "({0})".format(entry["description"][0])
    circumstance_data = entry["circumstances"]
    if entry["other_more"][0]:
        circumstance_data += entry["other_more"]
        circumstance_data.remove('other')
    formatted_circumstances = list(map(format_circumstance, circumstance_data))
    circumstances = ", ".join(formatted_circumstances)
    duration_dict = dict(forms.HistoryDetailsForm.DURATION_CHOICES)
    duration = duration_dict[entry["duration"][0]]
    return "For {0}: {1} {2}".format(duration, circumstances, description)


def format_circumstance(circumstance):
    circumstance_dict = dict(forms.HistoryDetailsForm.CIRCUMSTANCE_CHOICES)
    return circumstance_dict.get(circumstance, circumstance)


class HistoryDetailsView(FormView):
    """
    Render HistoryDetailsView and redirect to HistoryReportView when
    the form has been completed 3 times
    """

    template_name = "history/details.html"
    form_class = forms.HistoryDetailsForm

    def get(self, request, *args, **kwargs):
        if len(self.request.session.get('forms', [])) >= 3:
            url = reverse('history:report')
            return http.HttpResponseRedirect(url)
        else:
            response = super().get(request, *args, **kwargs)
            return response

    def form_valid(self, form):
        if 'forms' not in self.request.session:
            self.request.session['forms'] = []
        self.request.session['forms'] += [dict(form.data.lists())]
        if len(self.request.session['forms']) < 3:
            url = reverse('history:details')
        else:
            url = reverse('history:report')
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        history_data = get_form_data_from_session(self.request.session)
        if history_data:
            context['history'] = map(format_history_entry, history_data)
            context['circumstance_title'] = "Your circumstances previously"
        else:
            context['circumstance_title'] = "Your current circumstances"
        return context


class HistoryReportView(TemplateView):
    def get(self, request, *args, **kwargs):
        session = self.request.session
        if 'forms' not in session or len(session['forms']) < 3:
            url = reverse('history:details')
            return http.HttpResponseRedirect(url)
        else:
            self.template_name = "history/report.html"
            response = super().get(request, *args, **kwargs)
            return response

    def get_context_data(self, **kwargs):
        context = kwargs
        history_data = get_form_data_from_session(self.request.session)
        context['report'] = map(format_history_entry, history_data)
        return context
