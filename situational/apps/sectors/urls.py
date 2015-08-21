from django.conf.urls import url

from sectors import views
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


urlpatterns = [
    url(r'^$',
        views.SectorStartView.as_view(), name="start"),
    url(r'wizard/(?P<step>.+)/$', sector_wizard, name='wizard_step'),
    url(r'wizard/$', sector_wizard, name='wizard'),
]
