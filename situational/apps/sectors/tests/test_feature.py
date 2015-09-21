from django.core.urlresolvers import reverse
from django.core import mail

from splinter import Browser

from situational.testing import BaseCase


class TestSectors(BaseCase):
    def test_happy_path(self):
        with Browser("django") as b:
            b.visit(reverse("sectors:start"))
            b.click_link_by_text("Start")

            b.fill("sector_form-sector_0", "customer services")
            b.fill("sector_form-sector_1", "security")
            b.fill("sector_form-sector_2", "data entry")
            b.find_by_text("Next").first.click()

            checkboxes = b.find_by_css('.result-item input[type=checkbox]')
            self.assertTrue(checkboxes)
            for cb in checkboxes:
                cb._control.value = ['checked']
            b.find_by_text("Next").first.click()

            self.assertTrue(
                b.is_text_present(
                    "Please wait while we generate your report...")
            )
            b.reload()

            self.assertEqual(len(checkboxes), len(b.find_by_css(".job_item")))

            b.fill("email", "test@example.org")
            b.find_by_value("Send").first.click()
            self.assertTrue(
                b.is_text_present(
                    "Your report has been sent to test@example.org")
            )
            self.assertEqual(len(mail.outbox), 1)
