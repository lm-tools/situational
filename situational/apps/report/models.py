from travel_times.models import TravelTimesMap
from travel_times.views import MapView
from travel_times.tasks import download_map_image


class Report():
    def __init__(self, postcode):
        self.postcode = postcode

    def populate_async(self):
        download_map_image.delay(self.travel_times_map)

    @property
    def travel_times_map(self):
        if not hasattr(self, '_travel_times_map'):
            travel_times_map, _created = TravelTimesMap.objects.get_or_create(
                postcode=self.postcode,
                width=MapView.default_width,
                height=MapView.default_height,
                )
            self._travel_times_map = travel_times_map
        return self._travel_times_map

    @property
    def is_populated(self):
        return self.travel_times_map.has_image
