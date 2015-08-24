import datetime

from django import http
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View

from . import forms
from . import pdf
from . import tasks


def format_summary(session):
    result = {}
    current = session.get('current_work')
    training_data = session.get('training_education')
    data_2015 = session.get('work_2015')
    data_2014 = session.get('work_2014')
    before_2014 = session.get('before_2014')
    other_circumstances = session.get('other')
    if current:
        result['current'] = format_current_status(current)
    if training_data:
        result['training'] = format_training_data(training_data)
    if data_2015:
        result['2015'] = format_year_change_data(data_2015, 2015)
    if data_2014:
        result['2014'] = format_year_change_data(data_2014, 2014)
    if before_2014:
        result['before'] = format_before_data(before_2014)
    if other_circumstances:
        result['other'] = format_other_circumstances(other_circumstances)
    return result


def format_before_data(before_data):
    result = {}
    if before_data.get('text', None):
        result["text"] = before_data["text"][0]
    return result


def format_other_circumstances(other_circumstances):
    result = {}
    if other_circumstances.get('text', None):
        result["text"] = other_circumstances["text"][0]
    return result


def format_current_status(current):
    result = {}
    if current.get('status', None):
        result["status"] = format_status(current['status'][0])
    if current.get('description', None):
        result["description"] = current["description"][0]
    return result


def format_training_data(training_education):
    result = {}
    current = training_education.get("yes_or_no", ["unknown"])[0]
    if current == "yes":
        result["current"] = "You are currently in training or education."
    elif current == "no":
        result["current"] = "You are not currently in training or education."
    if training_education.get("current", None):
        result["current_info"] = training_education.get("current")[0]
    if training_education.get("previous", None):
        result["previous_info"] = training_education.get("previous")[0]
    return result


def format_year_change_data(year_change, year):
    result = {}
    current = year_change.get("changes", ["unknown"])[0]
    if current == "yes":
        result["current"] = \
            "Your work status has changed in {0}.".format(year)
    elif current == "no":
        result["current"] = \
            "Your work status has not changed in {0}.".format(year)
    if year_change.get("description", None):
        result["description"] = year_change.get("description")[0]
    return result


def remove_csrf_token(data):
    if data:
        data.pop("csrfmiddlewaretoken", None)
    return data


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


def format_status(status):
    status_dict = dict(forms.CurrentWorkStatusForm.WORK_STATUS_CHOICES)
    return status_dict.get(status, status)


def get_employment_context(session):
    current = session.get('current_work')
    if current:
        status = current.get('status', ['unknown'])[0]
        return status in ['full_time', 'part_time', 'work_programme']
    else:
        return False


class StartView(TemplateView):
    template_name = "detailed_history/start.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class CurrentWorkView(FormView):
    template_name = "detailed_history/current_work.html"
    form_class = forms.CurrentWorkStatusForm

    def form_valid(self, form):
        self.request.session['current_work'] = dict(form.data.lists())
        url = reverse('detailed_history:work_change_1')
        return http.HttpResponseRedirect(url)


class WorkChangeOneView(FormView):
    template_name = "detailed_history/work_change_1.html"
    form_class = forms.PreviousYearsForm

    def form_valid(self, form):
        self.request.session['work_2015'] = dict(form.data.lists())
        url = reverse('detailed_history:work_change_2')
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        context['employed'] = get_employment_context(self.request.session)
        return context


class WorkChangeTwoView(FormView):
    template_name = "detailed_history/work_change_2.html"
    form_class = forms.PreviousYearsForm

    def form_valid(self, form):
        self.request.session['work_2014'] = dict(form.data.lists())
        work_1 = self.request.session['work_2015'].get('changes', ['no'])[0]
        work_2 = self.request.session['work_2014'].get('changes', ['no'])[0]
        if (work_1 == 'no' and work_2 == 'no'):
            url = reverse('detailed_history:work_previous')
        else:
            url = reverse('detailed_history:training_education')
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        context['employed'] = get_employment_context(self.request.session)
        return context


class WorkPreviousView(FormView):
    template_name = "detailed_history/work_previous.html"
    form_class = forms.OneTextFieldForm

    def form_valid(self, form):
        self.request.session['before_2014'] = dict(form.data.lists())
        url = reverse('detailed_history:training_education')
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        context['employed'] = get_employment_context(self.request.session)
        return context


class TrainingEducationView(FormView):
    template_name = "detailed_history/training_education.html"
    form_class = forms.TrainingEducationForm

    def form_valid(self, form):
        self.request.session['training_education'] = dict(form.data.lists())
        url = reverse('detailed_history:other_circumstances')
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        context['employed'] = get_employment_context(self.request.session)
        return context


class OtherCircumstancesView(FormView):
    template_name = "detailed_history/other_circumstances.html"
    form_class = forms.OneTextFieldForm

    def form_valid(self, form):
        self.request.session['other'] = dict(form.data.lists())
        url = reverse('detailed_history:summary')
        return http.HttpResponseRedirect(url)


class SummaryView(TemplateView):
    template_name = "detailed_history/summary.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        context['summary'] = format_summary(self.request.session)
        return context


class SendView(TemplateView):
    template_name = "detailed_history/send.html"

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        history = format_summary(self.request.session)
        tasks.send_detailed_history.delay(history, email)
        return self.get(request, *args, **kwargs)


class PDFView(View):
    def get(self, request, *args, **kwargs):
        history = format_summary(self.request.session)
        pdf_contents = pdf.render(history)
        response = http.HttpResponse(pdf_contents, 'application/pdf')
        response['Content-Disposition'] = "filename=history-summary.pdf"
        return response
