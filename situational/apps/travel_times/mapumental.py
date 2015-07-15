import os

import requests

from django.conf import settings


class Client(object):
    def __init__(self):
        self.api_key = settings.MAPUMENTAL_API_KEY

    def get(self, postcode, width, height, depart_at, arrive_before):
        url = 'https://api.mapumental.com/static_map/'
        params = self._params({
            "postcodes": postcode,
            "direction": "depart_after",
            "time": depart_at,
            "limit_time": arrive_before,
            "width": width,
            "height": height,
        })
        response = requests.get(url, params=params)
        return Image(response.content, response.headers.get("content-type"))

    def _params(self, extra={}):
        params = {
            "api_key": self.api_key
        }
        params.update(extra)
        return params


class Image(object):
    def __init__(self, data, mime_type):
        self.data = data
        self.mime_type = mime_type


class FakeClient(object):
    def get(self, *args, **kwargs):
        image_path = os.path.join(
            os.path.dirname(__file__),
            'mapumental_dummy_map_N41AA.png',
            )
        image_data = open(image_path, 'rb').read()
        return Image(image_data, 'image/png')
