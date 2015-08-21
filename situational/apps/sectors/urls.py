from django.conf.urls import url

from . import views
from .forms import SectorForm, JobDescriptionsForm, SOCCodesView

named_form_steps = (
    ('sector_form', SectorForm),
    ('job_descriptions_form', JobDescriptionsForm),
)

sector_wizard = views.SectorWizardView.as_view(
    named_form_steps,
    url_name='sectors:wizard_step'
)

report_id = "(?P<report_id>\d+)"

urlpatterns = [
    url(r'^$',
        views.SectorStartView.as_view(), name="start"),
    url(r'wizard/(?P<step>.+)/$', sector_wizard, name='wizard_step'),
    url(r'wizard/$', sector_wizard, name='wizard'),
    url(r'soc_codes/' + report_id + '$',
        views.ReportView.as_view(),
        name="report"),
    url(r'soc_codes/' + report_id + '.pdf$',
        views.PDFView.as_view(),
        name="pdf"),
    url(r'soc_codes/' + report_id +
        '/populated_result_fields.json$',
        views.PopulatedResultFieldsView.as_view(),
        name="populated_result_fields"),
    url(r'soc_codes/' + report_id + '/send$',
        views.SendReportView.as_view(),
        name="send_report"),
]
