from django.test import TestCase

from travel_times.models import TravelTimesMap
from travel_times.tasks import download_map_image


class TestCelery(TestCase):
    def test_download_image(self):
        test_map = TravelTimesMap(
            postcode="SW1A1AA",
            width=100,
            height=100
        )
        test_map.save()
        download_map_image(test_map)
        test_map.refresh_from_db()
        self.assertTrue(test_map.image)

