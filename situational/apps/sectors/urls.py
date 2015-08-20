from django.conf.urls import url

from . import views
from .forms import SectorForm, JobDescriptionsForm, SOCCodesView

named_form_steps = (
    ('sector_form', SectorForm),
    ('job_descriptions_form', JobDescriptionsForm),
    ('soc_codes_form', SOCCodesView),
)

sector_wizard = views.SectorWizardView.as_view(
    named_form_steps,
    url_name='sectors:wizard_step'
)

postcode = "(?P<postcode>[a-zA-Z0-9\s]+)"
soc_codes = "(?P<soc_codes>[-\w\s]+(?:,[-\w\s]*)*)"

urlpatterns = [
    url(r'^$',
        views.SectorStartView.as_view(), name="start"),
    url(r'wizard/(?P<step>.+)/$', sector_wizard, name='wizard_step'),
    url(r'wizard/$', sector_wizard, name='wizard'),
    url(r'soc_codes$', views.SOCCodesView.as_view(),
        name="soc_code_info"),
    url(r'soc_codes/' + postcode + '/' + soc_codes + '$',
        views.ReportView.as_view(),
        name="report"),
    url(r'soc_codes/' + postcode + '/' + soc_codes +
        '/populated_result_fields.json$',
        views.PopulatedResultFieldsView.as_view(),
        name="populated_result_fields"),
    url(r'soc_codes/' + postcode + '/' + soc_codes + '/send$',
        views.SendReportView.as_view(),
        name="send_report"),
]
