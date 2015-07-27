from django.db import models

from jsonfield import JSONField
from model_utils.models import TimeStampedModel

from travel_times.models import TravelTimesMap
from travel_times.views import MapView
from travel_times.tasks import download_map_image

from report import tasks


class Report(TimeStampedModel):
    postcode = models.CharField(blank=False, null=False, max_length=14)
    place_name = models.CharField(blank=True, max_length=255)
    location_json = JSONField()
    top_categories = JSONField()
    top_companies = JSONField()
    latest_jobs = JSONField()
    travel_times_map = models.ForeignKey(TravelTimesMap, null=True)
    is_populating = models.BooleanField(default=False)

    def populate_async(self):
        if not self.is_populating:
            self.is_populating = True
            self.save()
            tasks.populate_report.delay(self)

    def get_travel_times_map(self):
        if not self.travel_times_map:
            travel_times_map, _created = TravelTimesMap.objects.get_or_create(
                postcode=self.postcode,
                width=MapView.default_width,
                height=MapView.default_height,
            )
            self.travel_times_map = travel_times_map
            self.save()
        return self.travel_times_map

    @property
    def is_populated(self):
        self.refresh_from_db()
        all_populated = all((
            self.get_travel_times_map().has_image,
            self.place_name,
            self.location_json,
            self.top_categories != '',
            self.top_companies != '',
            self.latest_jobs != '',
        ))

        if all_populated and self.is_populating:
            self.is_populating = False
            self.save()
        return all_populated
