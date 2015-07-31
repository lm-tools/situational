from django.db import models

from jsonfield import JSONField
from model_utils.models import TimeStampedModel

from travel_times.models import TravelTimesMap

from report import tasks


class Report(TimeStampedModel):
    postcode = models.CharField(blank=False, null=False, max_length=14)
    location_json = JSONField()
    top_categories = JSONField()
    top_companies = JSONField()
    latest_jobs = JSONField()
    travel_times_map = models.ForeignKey(TravelTimesMap, null=True)
    is_populating = models.BooleanField(default=False)

    RESULT_FIELDS = (
        'location_json',
        'top_categories',
        'top_companies',
        'latest_jobs',
        'travel_times_map',
    )

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
        if field == 'travel_times_map':
            return self.travel_times_map and self.travel_times_map.has_image
        else:
            return getattr(self, field) != ''
