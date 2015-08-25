from django import http
from django.core.urlresolvers import reverse
from django.utils.dates import MONTHS
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from . import forms, helpers, session_helpers, tasks, pdf


def format_circumstance(circumstance):
    circumstance_dict = dict(forms.HistoryDetailsForm.CIRCUMSTANCE_CHOICES)
    return circumstance_dict.get(circumstance, circumstance)


def format_timeline_data(session):
    result = {}
    timeline_beginning = session_helpers.last_known_start_date(session)
    timeline_end = session_helpers.formatted_now()
    result["items"] = []
    for history_item in session['quick_history']:
        item = {}
        circumstance = helpers.format_circumstance(
            history_item["circumstances"]
        )
        label = circumstance
        if history_item["description"]:
            label += " ({})".format(description)
        item["description"] = label
        item["intervals"] = helpers.intervals_for_item(
            history_item,
            timeline_beginning,
            timeline_end
        )
        result["items"] += [item]
    result["years"] = helpers.year_timeline(
        timeline_beginning,
        timeline_end
    )
    return result


def data_collection_started(session):
    if 'quick_history' not in session:
        return False
    else:
        return len(session['quick_history']) > 0


def number_months_collected(session):
    result = 0
    for history_item in session.get('quick_history', []):
        result += helpers.number_of_months_in_item(history_item)
    return result


def enough_data_collected(session):
    if 'quick_history' not in session:
        return False
    else:
        enough_items = len(session['quick_history']) >= 2
        enough_time = number_months_collected(session) >= 24
        return enough_items and enough_time


def store_data_in_session(session, form):
    if 'quick_history' not in session:
        session['quick_history'] = []
    last_known_start = session_helpers.last_known_start_date(session)
    quick_history_entry = {
        "description": form.data.get('description'),
        "circumstances": form.data.get('circumstances'),
        "from_month": int(form.data.get('date_month')),
        "from_year": int(form.data.get('date_year')),
        "to_month": last_known_start.get('month'),
        "to_year": session_helpers.last_known_start_date(session).get('year')
    }
    # Prepending to store data in chronological order, not order of entry
    session['quick_history'] = [quick_history_entry] + session['quick_history']
    return


def humanized_last_known_date(session):
    date = session_helpers.last_known_start_date(session)
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
    def get(self, request, *args, **kwargs):
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
