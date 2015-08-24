import datetime

from django import http
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from . import forms
from . import tasks
from . import pdf

#TODO: implement
def format_timeline_data(session):
# Timeline object:
# timeline.items = [item, item, ...]
# timeline.items has to be in chronological order (oldest item first)
# item.description = nicely-formatted-circumstance (description)
# item.intervals = [interval, interval] or [interval, interval, interval]
# interval.active = True or False
# interval.width = % of total length of timeline that interval should take
# timeline.years = [year, year, ...]
# timeline.years has to be in chronological order (oldest first)
# year.width = % of total length of timeline that year should take
# year.label = year number
    result = {}
    r
    return result

# TODO: True if data collection has started, False if not
def data_collection_started(session):
    return True

# TODO: True if at least 2 years and 2 things collected
def enough_data_collected(session):
    return False

# TODO: seems like a self-explanatory method title
def store_data_in_session(session, form):
    return

# TODO:
def humanized_last_known_date(session):
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
        last_known_date = humanized_last_known_date(session)
        if has_some_data:
            title = "Your work circumstances before {}".format(last_known_date)
        else:
            title = "Your current work circumstances"
        context['circumstance_title'] = title
        context['last_known_date'] = last_known_date
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
        context['timeline'] = format_timeline_data(self.request.session)
        return context


class ClearSessionView(TemplateView):
    def post(self, request, *args, **kwargs):
        self.request.session['forms'] = []
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
