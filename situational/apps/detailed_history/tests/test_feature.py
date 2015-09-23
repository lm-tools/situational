from django.core.urlresolvers import reverse
from django.core import mail

from splinter import Browser

from situational.testing import BaseCase


class TestDetailedHistory(BaseCase):
    def test_happy_path(self):
        with Browser("django") as b:
            b.visit(reverse("detailed_history:start"))
            b.click_link_by_text("Start")

            b.choose("status", "full_time")
            b.fill("description", "Stormtrooper, Galactic Empire")
            b.find_by_value("Next").first.click()

            b.choose("changes", "yes")
            b.fill("description", "TIE Fighter piloting, level 1")
            b.find_by_value("Next").first.click()

            b.choose("changes", "yes")
            b.fill("description", "Security guard, the Hutt")
            b.find_by_value("Next").first.click()

            b.choose("yes_or_no", "yes")
            b.fill("current", "TIE Fighter piloting, level 2")
            b.fill("previous", "TIE/LN engine maintenance")
            b.find_by_value("Next").first.click()

            b.fill("text", "Two-time podracing champion")
            b.find_by_value("Next").first.click()

            self.assertTrue(
                b.is_text_present("Tell your work coach your history"))
            self.assertTrue(b.is_text_present("Stormtrooper, Galactic Empire"))
            self.assertTrue(b.is_text_present("TIE Fighter piloting, level 1"))
            self.assertTrue(b.is_text_present("Security guard, the Hutt"))
            self.assertTrue(b.is_text_present("TIE Fighter piloting, level 2"))
            self.assertTrue(b.is_text_present("TIE/LN engine maintenance"))
            self.assertTrue(b.is_text_present("Two-time podracing champion"))

            b.fill("email", "test@example.org")
            b.find_by_value("Send").first.click()
            self.assertTrue(
                b.is_text_present(
                    "Your report has been sent to test@example.org")
            )
            self.assertEqual(len(mail.outbox), 1)
