from django.db import models

from jsonfield import JSONField
from model_utils.models import TimeStampedModel

import template_to_pdf
from sectors import tasks


class SectorsReport(TimeStampedModel):
    soc_codes = models.CharField(
        blank=False, null=False, max_length=200)
    soc_code_data = JSONField()

    RESULT_FIELDS = (
        'soc_code_data',
    )

    def to_pdf(self):
        template = template_to_pdf.Template('sectors/print.html')
        return template.render({'report': self})

    def send_to(self, email):
        tasks.send_report.delay(self, email)

    def populate_async(self):
        tasks.populate_report.delay(self)

    @property
    def is_populated(self):
        return all(
            self._is_result_field_populated(f) for f in self.RESULT_FIELDS
        )

    @property
    def populated_result_fields(self):
        return list(
            f for f in self.RESULT_FIELDS if self._is_result_field_populated(f)
        )

    def _is_result_field_populated(self, field):
        return getattr(self, field) != ''
