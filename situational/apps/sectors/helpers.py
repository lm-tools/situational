from operator import itemgetter

import requests

from django.conf import settings


class LMIForAllException(Exception):
    pass


class LMIForAllClient(object):
    def __init__(self):
        self.BASE_URL = settings.LMI_FOR_ALL_API_URL

    def base_request(self, endpoint, params=None):
        URL = "{0}{1}".format(self.BASE_URL, endpoint)
        req = requests.get(URL, params=params)

        # API returns 200 when it means 404.  Catch that.
        if req.status_code != 200 or not req.content:
            raise LMIForAllException('No content returned from API')

        req_json = req.json()

        if 'error' in req_json:
            raise LMIForAllException(req_json()['error'])

        return req_json

    def _clean_add_titles(self, titles):
        # Basic clean up of `add_titles`
        clean_titles = []
        for title in titles:
            if len(title) < 4 or '(' in title:
                continue
            if ',' in title:
                a, b = title.split(',', 1)
                title = " ".join((b, a))
            title = title.strip().title()
            clean_titles.append(title)
        return list(set(clean_titles))

    def keyword_search(self, keyword):
        BASE_URL = "http://api.lmiforall.org.uk/api/v1/soc/search"
        return requests.get(BASE_URL, params={'q': keyword}).json()

    def soc_code_info(self, soc_code):
        info = self.base_request("soc/code/{0}".format(soc_code))

        # Split tasks on newline
        info['tasks'] = [t.strip() for t in info['tasks'].split('\n')]
        info['add_titles'] = self._clean_add_titles(info['add_titles'])

        return info

    def hours_worked(self, soc_code):
        return self.base_request('ashe/estimateHours', {
            'soc': soc_code,
            'coarse': 'true'
        })['series'][0]['hours']

    def pay(self, soc_code):
        return self.base_request(
            "ashe/estimatePay", {
                'soc': soc_code,
                'coarse': 'true'
            }
        )['series'][0]['estpay']

    def jobs_breakdown(self, postcode):
        breakdown = self.base_request('census/jobs_breakdown', {
            'area': postcode
        })
        return sorted(
            breakdown['jobsBreakdown'],
            key=itemgetter('percentage'),
            reverse=True)[:5]

    def resident_occupations(self, postcode):
        occupations = self.base_request('census/resident_occupations', {
            'area': postcode
        })
        return sorted(
            occupations['residentOccupations'],
            key=itemgetter('percentage'),
            reverse=True)[:5]
