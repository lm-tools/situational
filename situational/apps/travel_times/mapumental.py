from io import BytesIO
import os

import requests

from django.conf import settings


class Client(object):
    def __init__(self):
        self.api_key = settings.MAPUMENTAL_API_KEY

    def get(self, postcode, width, height, depart_at, max_travel_time):
        url = 'https://api.mapumental.com/static_map/'
        params = self._params({
            "postcodes": postcode,
            "direction": "depart_after",
            "time": depart_at,
            "max_travel_time": max_travel_time,
            "colour_scheme": "08519c,3182bd,6baed6,9ecae1,c6dbef",
            "width": width,
            "height": height,
            "print_styles": "yes",
            "band_minutes": round(max_travel_time / 3),
            "show_legend": "no",
            "show_title": "no"
        })
        response = requests.get(url, params=params)
        image_data_io = BytesIO(response.content)
        return Image(image_data_io, response.headers.get("content-type"))

    def _params(self, extra={}):
        params = {
            "api_key": self.api_key
        }
        params.update(extra)
        return params


class Image(object):
    def __init__(self, file, mime_type):
        self.file = file
        self.mime_type = mime_type


class FakeClient(object):
    def get(self, *args, **kwargs):
        image_path = os.path.join(
            os.path.dirname(__file__),
            'mapumental_dummy_map_N41AA.png',
        )
        image_file = open(image_path, 'rb')
        return Image(image_file, 'image/png')
