from django.conf.urls import url

from . import views
from .forms import SectorForm, JobDescriptionsForm

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
    url(r'^$', sector_wizard, name='start'),
    url(r'(?P<step>.+)/$', sector_wizard, name='wizard_step'),
    url(r'soc_codes/' + report_id + '$',
        views.ReportView.as_view(),
        name="report"),
    url(r'soc_codes/' + report_id + '.pdf$',
        views.PDFView.as_view(),
        name="pdf"),
    url(r'soc_codes/' + report_id +
        '/is_populated.json$',
        views.IsPopulatedView.as_view(),
        name="is_populated"),
    url(r'soc_codes/' + report_id + '/send$',
        views.SendReportView.as_view(),
        name="send_report"),
]
