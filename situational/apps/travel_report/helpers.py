import csv
import io
from urllib.request import urlopen

import requests

from django.core.cache import cache
from django.conf import settings

from . import constants


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


def top_categories_for_postcode(postcode):
    base_url = settings.JOBS_API_BASE_URL
    url = "{0}/api/top_categories?postcode={1}".format(
        base_url,
        postcode,
    )

    return requests.get(url).json()


def latest_jobs_for_postcode(postcode):
    base_url = settings.JOBS_API_BASE_URL
    url = "{0}/api/jobadverts?postcode={1}".format(
        base_url,
        postcode,
    )

    return requests.get(url).json()


def top_companies_for_postcode(postcode):
    base_url = settings.JOBS_API_BASE_URL
    url = "{0}/api/top_companies?postcode={1}".format(
        base_url,
        postcode,
    )

    return requests.get(url).json()
