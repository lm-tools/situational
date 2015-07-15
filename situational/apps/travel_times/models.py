from django.conf import settings

from travel_times import mapumental


class TravelTimesMapRepository(object):
    def __init__(self, client=None):
        if not client:
            client = getattr(settings, 'MAPUMENTAL_CLIENT', mapumental.Client)
        self.client = client()
        self.depart_at = '0800'
        self.arrive_before = '0930'

    def get(self, postcode, width, height):
        image = self.client.get(
            postcode,
            width,
            height,
            self.depart_at,
            self.arrive_before,
            )
        return TravelTimesMap(
            postcode,
            width,
            height,
            image.data,
            image.mime_type,
            )


class TravelTimesMap(object):
    def __init__(self, postcode, width, height, image_data, mime_type):
        self.postcode = postcode
        self.width = width
        self.height = height
        self.image_data = image_data
        self.mime_type = mime_type
