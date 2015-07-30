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

    def populate_async(self):
        tasks.populate_report.delay(self)

    @property
    def is_populated(self):
        return all((
            self.travel_times_map and self.travel_times_map.has_image,
            self.location_json != '',
            self.top_categories != '',
            self.top_companies != '',
            self.latest_jobs != '',
        ))
