from unittest.mock import patch, PropertyMock

from django.core.urlresolvers import reverse

from travel_report import models
from situational.testing import BaseCase


class TestShowView(BaseCase):

    def test_get_with_populated_report(self):
        with patch('travel_report.models.TravelReport.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = True

            response = self.client.get(
                reverse('travel_report:show', kwargs={'postcode': 'SW1H0DJ'}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "travel_report/show.html")

    def test_get_with_unpopulated_report(self):
        with patch('travel_report.models.TravelReport.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = False

            response = self.client.get(
                reverse('travel_report:show', kwargs={'postcode': 'SW1H0DJ'}))
            self.assertEqual(response.status_code, 202)
            self.assertTemplateUsed(response, "travel_report/pending.html")


class TestSendView(BaseCase):
    def test_post(self):
        models.TravelReport.objects.create(postcode='SW1H0DJ')
        with patch('travel_report.models.TravelReport.send_to') as send_to:
            response = self.client.post(
                reverse('travel_report:send', kwargs={'postcode': 'SW1H0DJ'}),
                data={'email': 'test@example.org'}
            )
            send_to.assert_called_with('test@example.org')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'travel_report/send.html')
            self.assertEqual(response.context['postcode'], 'SW1H0DJ')
            self.assertEqual(response.context['email_address'],
                             'test@example.org')
