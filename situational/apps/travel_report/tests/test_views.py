from unittest.mock import patch, PropertyMock

from django.core.urlresolvers import reverse

from travel_report import models
from situational.testing import BaseCase


class TestReportView(BaseCase):

    def test_get_with_populated_report(self):
        with patch('travel_report.models.TravelReport.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = True

            response = self.client.get(
                reverse(
                    'travel_report:report',
                    kwargs={'postcode': 'SW1H0DJ'}
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "travel_report/report.html")

    def test_get_with_unpopulated_report(self):
        with patch('travel_report.models.TravelReport.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = False

            response = self.client.get(
                reverse(
                    'travel_report:report',
                    kwargs={'postcode': 'SW1H0DJ'}
                )
            )
            self.assertEqual(response.status_code, 202)
            self.assertTemplateUsed(response, "travel_report/pending.html")

    def test_send_report(self):
        models.TravelReport.objects.create(postcode='SW1H0DJ')
        with patch('travel_report.models.TravelReport.send_to') as send_to:
            response = self.client.post(
                reverse(
                    'travel_report:report',
                    kwargs={'postcode': 'SW1H0DJ'}
                ),
                data={'email': 'test@example.org'},
                follow=True
            )
            send_to.assert_called_with('test@example.org')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'travel_report/report.html')
            self.assertEqual(response.context['postcode'], 'SW1H0DJ')
            self.assertContains(self.response, 'test@example.org')
