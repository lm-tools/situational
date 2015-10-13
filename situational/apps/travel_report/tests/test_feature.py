from django.core.urlresolvers import reverse
from django.core import mail

from splinter import Browser

from situational.testing import BaseCase


class TestTravelReport(BaseCase):
    def test_happy_path(self):
        with Browser("django") as b:
            b.visit(reverse("travel_report:start"))
            b.fill("postcode", "SW1A 1AA")
            b.find_by_text("Start").first.click()
            self.assertTrue(
                b.is_text_present(
                    "Your map is loading")
            )
            b.reload()
            self.assertTrue(
                b.is_text_present(
                    "This map shows where you can get to from SW1A1AA")
            )
            self.assertTrue(
                b.find_by_css('.travel-map')
            )

            b.fill("email", "test@example.org")
            b.find_by_value("Send").first.click()
            self.assertTrue(
                b.is_text_present(
                    "Your report has been sent to test@example.org")
            )
            self.assertEqual(len(mail.outbox), 1)
