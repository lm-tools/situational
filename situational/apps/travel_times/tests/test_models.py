from django.test import TestCase

from travel_times.models import TravelTimesMap


class TestTravelTimesMap(TestCase):
    def test_download_image(self):
        test_map = TravelTimesMap.objects.create(
            postcode="SW1A1AA",
            width=100,
            height=100
        )
        test_map.download_image()
        test_map.refresh_from_db()
        self.assertTrue(test_map.image)
