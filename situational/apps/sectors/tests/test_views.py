from unittest.mock import patch, PropertyMock

from django.core.urlresolvers import reverse

from sectors import models
from situational.testing import BaseCase


class TestShowView(BaseCase):

    def test_get_with_populated_report(self):
        with patch('sectors.models.SectorsReport.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = True

            response = self.client.get(
                reverse(
                    'sectors:show',
                    kwargs={
                        'postcode': 'SW1H0DJ',
                        'soc_codes': '3114,5330'
                    }
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "sectors/report.html")

    def test_get_with_unpopulated_report(self):
        with patch('sectors.models.SectorsReport.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = False

            response = self.client.get(
                reverse(
                    'sectors:show',
                    kwargs={
                        'postcode': 'SW1H0DJ',
                        'soc_codes': '3114,5330'
                    }
                )
            )
            self.assertEqual(response.status_code, 202)
            self.assertTemplateUsed(response, "sectors/report_pending.html")


class TestSendView(BaseCase):
    def test_post(self):
        models.SectorReport.objects.create(
            postcode='SW1H0DJ',
            soc_codes='3114,5330'
        )
        with patch('sectors.models.SectorReport.send_to') as send_to:
            response = self.client.post(
                reverse(
                    'sectors:send_report',
                    kwargs={
                        'postcode': 'SW1H0DJ',
                        'soc_codes': '3114,5330'
                    }
                ),
                data={'email': 'test@example.org'}
            )
            send_to.assert_called_with('test@example.org')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'sectors/send_report.html')
            self.assertEqual(response.context['postcode'], 'SW1H0DJ')
            self.assertEqual(response.context['soc_codes'], '3114,5330')
