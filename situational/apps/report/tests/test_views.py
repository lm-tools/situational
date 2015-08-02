from unittest.mock import patch, PropertyMock

from django.core.urlresolvers import reverse

from situational.testing import BaseCase


class TestReportView(BaseCase):

    def test_get_with_populated_report(self):
        with patch('report.models.Report.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = True

            response = self.client.get(
                reverse('report_view', kwargs={'postcode': 'SW1H0DJ'}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "report/report_view.html")

    def test_get_with_unpopulated_report(self):
        with patch('report.models.Report.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = False

            response = self.client.get(
                reverse('report_view', kwargs={'postcode': 'SW1H0DJ'}))
            self.assertEqual(response.status_code, 202)
            self.assertTemplateUsed(response, "report/report_pending.html")
