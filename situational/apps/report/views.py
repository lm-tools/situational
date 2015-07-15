from django import http
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.views.generic import FormView

from report import helpers
from report import forms


class PostcodeLookupView(FormView):
    """
    Render PostcodeForm and redirect to ReportView when the form is valid.
    """

    template_name = "report/postcode_view.html"
    form_class = forms.PostcodeForm

    def form_valid(self, form):
        postcode = form.cleaned_data['postcode'].upper().replace(' ', '')
        url = reverse('report_view', kwargs={'postcode': postcode})
        return http.HttpResponseRedirect(url)


class ReportView(TemplateView):
    template_name = "report/report_view.html"

    def get_context_data(self, **kwargs):
        context = kwargs
        context['location'] = helpers.geocode(context['postcode'])
        context['place_name'] = \
            helpers.place_name_from_location(**context['location'])
        return context
