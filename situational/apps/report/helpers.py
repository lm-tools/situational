import csv
import io
from urllib.request import urlopen

import requests

from django.core.cache import cache

from report import constants


class PostcodeNotFoundException(Exception):
    pass


def geocode(postcode):
    """
    Use MaPit to convert the postcode to a location.

    Assumes a valid postcode
    """
    cached = cache.get(postcode)
    if cached:
        return cached
    try:
        res = requests.get("%s/postcode/%s" % (constants.MAPIT_URL, postcode))
        res_json = res.json()
        if 'code' in res_json and res_json['code'] == 404:
            raise PostcodeNotFoundException("MaPit 404")
        else:
            lat = res_json['wgs84_lat']
            lon = res_json['wgs84_lon']

        result = {
            'wgs84_lon': lon,
            'wgs84_lat': lat,
        }
    except:
        result = None
    cache.set(postcode, result, 60 * 60 * 24)
    return result


def place_name_from_location(wgs84_lat, wgs84_lon):

    url = "{base_url}?f=get_places_near;lat={lat};lon={lon};number=100;distance=5".format(
        base_url=constants.GAZE_URL,
        lat=wgs84_lat,
        lon=wgs84_lon,
    )

    results = csv.DictReader(io.TextIOWrapper(urlopen(url)))
    for result in results:
        return result
