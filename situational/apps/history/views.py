import datetime
from django import http
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View
from history import forms


def get_form_data_from_session(session):
    form_data = session.get('forms', [])
    for form in form_data:
        form.pop("csrfmiddlewaretoken", None)
    return form_data


def format_summary(session):
    summary_keys = [
        'work_2015',
        'work_2015',
        'training_education',
        'other_circumstances'
    ]
    result = {key: remove_csrf_token(session.get(key)) for key in summary_keys}
    return result


def remove_csrf_token(data):
    if data:
        data.pop("csrfmiddlewaretoken", None)
    return data


def format_timeline_data(history_data):
    nb_months = total_number_of_months(history_data)
    result = {}
    result["years"] = timeline_years_dict(nb_months)
    result["timeline"] = circumstance_timeline(history_data, nb_months)
    return result


def total_number_of_months(history_data):
    result = 0
    for entry in history_data:
        result += length_in_months(entry)
    return result


def circumstance_timeline(history_data, nb_months):
    result = {}
    unique_circumstances = []
    circumstances = []
    for entry in history_data:
        circumstances += format_circumstances(entry)
    unique_circumstances = unique_items_from_list(circumstances)
    for unique_circumstance in unique_circumstances:
        result[unique_circumstance] = []
        for entry in history_data:
            duration = length_in_months(entry)
            active = unique_circumstance in format_circumstances(entry)
            result[unique_circumstance] += [
                {"length": duration / nb_months * 100, "active": active}
            ]
    return result


def length_in_months(entry):
    duration_length_dict = dict(forms.HistoryDetailsForm.DURATION_LENGTHS)
    duration = duration_length_dict[entry["duration"][0]]
    return duration


def unique_items_from_list(list_with_dups):
    result = []
    [result.append(i) for i in list_with_dups if i not in result]
    return result


def timeline_years_dict(nb_of_months):
    years = []
    now = datetime.datetime.now()
    year = now.year
    number_of_months = 0
    months_to_display = min(now.month, nb_of_months)
    while (number_of_months < nb_of_months):
        years += [
            {"label": year, "width": months_to_display / nb_of_months * 100}
        ]
        year -= 1
        number_of_months += months_to_display
        months_to_display = min(12, nb_of_months - number_of_months)
    return years


def format_circumstances(entry):
    circumstance_data = entry["circumstances"][:]
    if 'other' in circumstance_data:
        circumstance_data.remove('other')
    if entry["other_more"][0]:
        circumstance_data += entry["other_more"]
    formatted_circumstances = list(map(format_circumstance, circumstance_data))
    return formatted_circumstances


def format_circumstance(circumstance):
    circumstance_dict = dict(forms.HistoryDetailsForm.CIRCUMSTANCE_CHOICES)
    return circumstance_dict.get(circumstance, circumstance)


def history_entry_as_string(entry):
    description = ""
    if entry["description"][0]:
        description = "({0})".format(entry["description"][0])
    formatted_circumstances = format_circumstances(entry)
    circumstances = ", ".join(formatted_circumstances)
    duration_dict = dict(forms.HistoryDetailsForm.DURATION_CHOICES)
    duration = duration_dict[entry["duration"][0]]
    return "For {0}: {1} {2}".format(duration, circumstances, description)


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
            context['history'] = map(history_entry_as_string, history_data)
            context['circumstance_title'] = "Your circumstances previously"
            context['percentage'] = len(history_data) * 100 / 3
        else:
            context['circumstance_title'] = "Your current circumstances"
            context['percentage'] = 0
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
        context['report'] = map(history_entry_as_string, history_data)
        context['timeline'] = format_timeline_data(history_data)
        return context


class ClearSessionView(TemplateView):
    def post(self, request, *args, **kwargs):
        self.request.session['forms'] = []
        url = reverse('history:details')
        return http.HttpResponseRedirect(url)


class HistoryStartView(TemplateView):
    def get(self, request, *args, **kwargs):
        self.template_name = "history/start_text.html"
        response = super().get(request, *args, **kwargs)
        return response


class HistoryStartStructuredView(TemplateView):
    def get(self, request, *args, **kwargs):
        self.template_name = "history/start_structured.html"
        response = super().get(request, *args, **kwargs)
        return response


class CurrentWorkView(FormView):
    template_name = "history/current_work.html"
    form_class = forms.CurrentWorkStatusForm

    def form_valid(self, form):
        self.request.session['current_work'] = dict(form.data.lists())
        url = reverse('history:work_change_1')
        return http.HttpResponseRedirect(url)


class WorkChangeOneView(FormView):
    template_name = "history/work_change_1.html"
    form_class = forms.PreviousYearsForm

    def form_valid(self, form):
        self.request.session['work_2015'] = dict(form.data.lists())
        url = reverse('history:work_change_2')
        return http.HttpResponseRedirect(url)


class WorkChangeTwoView(FormView):
    template_name = "history/work_change_2.html"
    form_class = forms.PreviousYearsForm

    def form_valid(self, form):
        self.request.session['work_2014'] = dict(form.data.lists())
        work_1 = self.request.session['work_2015'].get('changes', ['no'])[0]
        work_2 = self.request.session['work_2014'].get('changes', ['no'])[0]
        if (work_1 == 'no' and work_2 == 'no'):
            url = reverse('history:work_previous')
        else:
            url = reverse('history:training_education')
        return http.HttpResponseRedirect(url)


class WorkPreviousView(FormView):
    template_name = "history/work_previous.html"
    form_class = forms.OneTextFieldForm

    def form_valid(self, form):
        self.request.session['before_2014'] = dict(form.data.lists())
        url = reverse('history:training_education')
        return http.HttpResponseRedirect(url)


class TrainingEducationView(FormView):
    template_name = "history/training_education.html"
    form_class = forms.TrainingEducationForm

    def form_valid(self, form):
        self.request.session['training_education'] = dict(form.data.lists())
        url = reverse('history:other_circumstances')
        return http.HttpResponseRedirect(url)


class OtherCircumstancesView(FormView):
    template_name = "history/other_circumstances.html"
    form_class = forms.OneTextFieldForm

    def form_valid(self, form):
        self.request.session['other'] = dict(form.data.lists())
        url = reverse('history:summary')
        return http.HttpResponseRedirect(url)


class SummaryView(TemplateView):
    def get(self, request, *args, **kwargs):
        self.template_name = "history/summary.html"
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        context['summary'] = format_summary(self.request.session)
        return context
