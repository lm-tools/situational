from django.db import models

from model_utils.models import TimeStampedModel

import template_to_pdf
from travel_times.models import TravelTimesMap

from . import tasks


class TravelReport(TimeStampedModel):
    postcode = models.CharField(
        blank=False, null=False, max_length=14, db_index=True)
    travel_times_map = models.ForeignKey(TravelTimesMap, null=True)

    RESULT_FIELDS = (
        'travel_times_map',
    )

    def to_pdf(self):
        template = template_to_pdf.Template('travel_report/print.html')
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

    def _is_result_field_populated(self, field):
        if field == 'travel_times_map':
            return self.travel_times_map and self.travel_times_map.has_image
        else:
            return getattr(self, field) != ''
