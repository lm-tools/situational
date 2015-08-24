import datetime

from django import http
from django.core.urlresolvers import reverse
from django.utils.dates import MONTHS
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from . import forms
from . import tasks
from . import pdf


# TODO: implement
def format_timeline_data(session):
    result = {}
    result["items"] = []
    for history_item in session['quick_history']:
        item = {}
        active_interval = {
            "active": True,
            "width": "30"
        }
        inactive_interval = {
            "active": False,
            "width": "70"
        }
        item["intervals"] = [active_interval, inactive_interval]
        circumstance = history_item["circumstances"]  # TODO: FORMAT
        description = history_item["description"]
        label = "{} ({})".format(circumstance, description)
        item["description"] = label
        result["items"] += [item]
    year_2014 = {
        "width": "60",
        "label": "2014"
    }
    year_2015 = {
        "width": "40",
        "label": "2015"
    }
    result["years"] = [year_2014, year_2015]
    return result


def data_collection_started(session):
    if 'quick_history' not in session:
        return False
    else:
        return len(session['quick_history']) > 0


# TODO: True if at least 2 years and 2 things collected
def enough_data_collected(session):
    if 'quick_history' not in session:
        return False
    else:
        return len(session['quick_history']) > 2


# TODO: either from session or current time
def get_end_date(session):
    return {
        "month": "8",
        "year": "2015"
    }


def store_data_in_session(session, form):
    if 'quick_history' not in session:
        session['quick_history'] = []
    quick_history_entry = {
        "description": form.data.get('description'),
        "circumstances": form.data.get('circumstances'),
        "from_month": form.data.get('date_month'),
        "from_year": form.data.get('date_year'),
        "to_month": get_end_date(session).get('month'),
        "to_year": get_end_date(session).get('year')
    }
    session['quick_history'] += [quick_history_entry]
    return


def humanized_last_known_date(session):
    date = get_end_date(session)
    return "{} {}".format(MONTHS[int(date["month"])], date["year"])
    return "Narnia o' clock"


class HistoryDetailsView(FormView):
    template_name = "quick_history/details.html"
    form_class = forms.HistoryDetailsForm

    def get(self, request, *args, **kwargs):
        if enough_data_collected(self.request.session):
            url = reverse('quick_history:report')
            return http.HttpResponseRedirect(url)
        else:
            response = super().get(request, *args, **kwargs)
            return response

    def form_valid(self, form):
        store_data_in_session(self.request.session, form)
        if enough_data_collected(self.request.session):
            url = reverse('quick_history:report')
        else:
            url = reverse('quick_history:details')
        return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        session = self.request.session
        has_some_data = data_collection_started(session)
        if has_some_data:
            last_known_date = humanized_last_known_date(session)
            title = "Your work circumstances before {}".format(last_known_date)
            context['last_known_date'] = last_known_date
        else:
            title = "Your current work circumstances"
            context['last_known_date'] = "now"
        context['circumstance_title'] = title
        return context


class HistoryReportView(TemplateView):
    template_name = "quick_history/report.html"

    def get(self, request, *args, **kwargs):
        if enough_data_collected(self.request.session):
            response = super().get(request, *args, **kwargs)
            return response
        else:
            url = reverse('quick_history:details')
            return http.HttpResponseRedirect(url)

    def get_context_data(self, **kwargs):
        context = kwargs
        context['timeline'] = format_timeline_data(self.request.session)
        return context


class ClearSessionView(TemplateView):
    def post(self, request, *args, **kwargs):
        self.request.session['quick_history'] = []
        url = reverse('quick_history:start')
        return http.HttpResponseRedirect(url)


class StartView(TemplateView):
    template_name = "quick_history/start.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return response


class SendView(TemplateView):
    template_name = "quick_history/send.html"

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        data = {}
        history_data = get_form_data_from_session(self.request.session)
        data['report'] = map(history_entry_as_string, history_data)
        data['timeline'] = format_timeline_data(history_data)
        tasks.send_quick_history.delay(data, email)
        return self.get(request, *args, **kwargs)


class PDFView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        history_data = get_form_data_from_session(self.request.session)
        data['report'] = map(history_entry_as_string, history_data)
        data['timeline'] = format_timeline_data(history_data)
        pdf_contents = pdf.render(data)
        response = http.HttpResponse(pdf_contents, 'application/pdf')
        response['Content-Disposition'] = "filename=history-summary.pdf"
        return response
