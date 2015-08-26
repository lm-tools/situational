"""
Helper class for working with the adzuna API
Copied from lm-tools-jobs-api
"""

import requests

from django.conf import settings


class Adzuna(object):
    def __init__(self):
        self.APP_ID = getattr(settings, 'ADZUNA_APP_ID')
        self.APP_KEY = getattr(settings, 'ADZUNA_APP_KEY')
        self.BASE_URL = "http://api.adzuna.com:80/v1/api/"

        assert all((self.APP_ID, self.APP_KEY))

    def _base_request(self, endpoint, params, page=None):
        URL = "{0}{1}".format(self.BASE_URL, endpoint)
        if page:
            URL = "{0}{1}".format(URL, page)

        params.update({
            "app_id": self.APP_ID,
            "app_key": self.APP_KEY,
        })

        req = requests.get(URL, params=params)

        if req.status_code != 200:
            raise ValueError("Got a {0} from Adzuna: {1}".format(
                req.status_code,
                req.json()['display']))
        return req

    def _unwrap_pagination(self, endpoint, params, count):
        num_results = 0
        page = 1

        while num_results <= count:
            results = self._base_request(endpoint, params, page)
            all_results = results.json().get('results', [])

            for result in all_results:
                if num_results < count:
                    num_results += 1
                    yield result
                else:
                    raise StopIteration
            page += 1

    def locations_for_postcode(self, postcode):
        endpoint = "jobs/gb/geodata/"
        params = {
            "where": postcode,
        }
        results = self._base_request(endpoint, params)
        area = results.json()['location']['area']
        assert (len(area) >= 3)
        locations = area[:3]
        return locations

    def jobs_at_location(self, location0, location1, location2, count=10):
        endpoint = "jobs/gb/search/"

        params = {
            "location0": location0,
            "location1": location1,
            "location2": location2,
            "sort_direction": "down",
            "sort_by": "date",
        }

        return self._unwrap_pagination(endpoint, params, count)

    def top_companies(self, location0, location1, location2, count=10):
        endpoint = "jobs/gb/top_companies/"

        params = {
            "location0": location0,
            "location1": location1,
            "location2": location2,
        }
        results = self._base_request(endpoint, params)
        return results.json()['leaderboard'][:count]
