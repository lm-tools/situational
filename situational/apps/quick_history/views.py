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


def format_circumstance(circumstance):
    circumstance_dict = dict(forms.HistoryDetailsForm.CIRCUMSTANCE_CHOICES)
    return circumstance_dict.get(circumstance, circumstance)


def format_timeline_data(session):
    result = {}
    timeline_beginning = last_known_start_date(session)
    timeline_end = now()
    result["items"] = []
    for history_item in session['quick_history']:
        item = {}
        circumstance = format_circumstance(history_item["circumstances"])
        description = history_item["description"]
        label = "{} ({})".format(circumstance, description)
        item["description"] = label
        item["intervals"] = intervals_for_item(
            history_item,
            timeline_beginning,
            timeline_end
        )
        result["items"] += [item]
    result["years"] = year_timeline(
        timeline_beginning,
        timeline_end
    )
    return result


def same_date(month_1, year_1, month_2, year_2):
    return (month_1 == month_2) and (year_1 == year_2)


def intervals_for_item(history_item, timeline_beginning, timeline_end):
    number_active_months = number_of_months(history_item)
    total_months = number_of_months(
        {
            "from_month": timeline_beginning["month"],
            "from_year": timeline_beginning["year"],
            "to_month": timeline_end["month"],
            "to_year": timeline_end["year"]
        }
    )
    if same_date(
        timeline_beginning["month"],
        timeline_beginning["year"],
        history_item["from_month"],
        history_item["from_year"]
    ):
        active_interval = {
            "active": True,
            "width": number_active_months / total_months * 100
        }
        inactive_interval = {
            "active": False,
            "width": 100 - active_interval["width"]
        }
        return [active_interval, inactive_interval]
    elif same_date(
        timeline_end["month"],
        timeline_end["year"],
        history_item["to_month"],
        history_item["to_year"]
    ):
        active_interval = {
            "active": True,
            "width": number_active_months / total_months * 100
        }
        inactive_interval = {
            "active": False,
            "width": 100 - active_interval["width"]
        }
        return [inactive_interval, active_interval]
    else:
        inactive_initial_months = number_of_months(
            {
                "from_month": timeline_beginning["month"],
                "from_year": timeline_beginning["year"],
                "to_month": history_item["from_month"],
                "to_year": history_item["from_year"]
            }
        )
        inactive_interval_1 = {
            "active": False,
            "width": inactive_initial_months / total_months * 100
        }
        active_interval = {
            "active": True,
            "width": number_active_months / total_months * 100
        }
        inactive_interval_2 = {
            "active": False,
            "width": 100 - active_interval["width"] - inactive_interval_1["width"]
        }
        return [inactive_interval_1, active_interval, inactive_interval_2]


def year_timeline(timeline_beginning, timeline_end):
    years = []
    total_months = number_of_months(
        {
            "from_month": timeline_beginning["month"],
            "from_year": timeline_beginning["year"],
            "to_month": timeline_end["month"],
            "to_year": timeline_end["year"]
        }
    )
    years += [{
        "width": (12 - timeline_beginning["month"]) / total_months * 100,
        "label": timeline_beginning["year"]
    }]
    for year in range(timeline_beginning["year"] + 1, timeline_end["year"]):
        years += [{
            "width": 12 / total_months * 100,
            "label": year
        }]
    years += [{
        "width": timeline_end["month"] / total_months * 100,
        "label": timeline_end["year"]
    }]
    return years


def data_collection_started(session):
    if 'quick_history' not in session:
        return False
    else:
        return len(session['quick_history']) > 0


def number_of_months(history_item):
    start_month = history_item["from_month"]
    start_year = history_item["from_year"]
    end_month = history_item["to_month"]
    end_year = history_item["to_year"]
    if start_month == end_month and start_year == end_year:
        return 1
    else:
        return (end_year - start_year) * 12 + (end_month - start_month)


def number_months_collected(session):
    result = 0
    for history_item in session.get('quick_history', []):
        result += number_of_months(history_item)
    return result


def enough_data_collected(session):
    if 'quick_history' not in session:
        return False
    else:
        enough_items = len(session['quick_history']) >= 2
        enough_time = number_months_collected(session) >= 24
        return enough_items and enough_time


def now():
    today = datetime.datetime.now()
    now = {
        "month": today.month,
        "year": today.year,
    }
    return now


def last_known_start_date(session):
    if 'quick_history' not in session or len(session['quick_history']) == 0:
        return now()
    else:
        oldest_known_item = session['quick_history'][0]
        return {
            "month": oldest_known_item["from_month"],
            "year": oldest_known_item["from_year"]
        }


def store_data_in_session(session, form):
    if 'quick_history' not in session:
        session['quick_history'] = []
    quick_history_entry = {
        "description": form.data.get('description'),
        "circumstances": form.data.get('circumstances'),
        "from_month": int(form.data.get('date_month')),
        "from_year": int(form.data.get('date_year')),
        "to_month": last_known_start_date(session).get('month'),
        "to_year": last_known_start_date(session).get('year')
    }
    # Prepending to store data in chronological order, not order of entry
    session['quick_history'] = [quick_history_entry] + session['quick_history']
    return


def humanized_last_known_date(session):
    date = last_known_start_date(session)
    return "{} {}".format(MONTHS[int(date["month"])], date["year"])


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
        # TODO: check since date is the past
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
