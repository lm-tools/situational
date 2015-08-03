from django.core.urlresolvers import reverse

from situational.testing import BaseCase


class TestConfidenceReport(BaseCase):
    def test_view_new_confidence_report_page(self):
        response = self.client.get(reverse('confidence:new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confidence/new.html")

    def test_view_confidence_report_page(self):
        response = self.client.get(reverse('confidence:show'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "confidence/show.html")
