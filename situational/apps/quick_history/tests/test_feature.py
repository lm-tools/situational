import datetime

from django.core.urlresolvers import reverse
from django.core import mail

from splinter import Browser

from situational.testing import BaseCase


class TestQuickHistory(BaseCase):
    def test_happy_path(self):
        with Browser("django") as b:
            b.visit(reverse("quick_history:start"))
            b.find_by_value("Start").first.click()

            now = datetime.datetime.now()
            month = (now.month % 12) + 1  # next month, with wraparound
            year = now.year
            b.choose("circumstances", "full_time")
            b.fill("description", "Stormtrooper, Galactic Empire")
            b.select("date_month", "%s" % month)
            b.select("date_year", "%s" % (year - 1))
            b.find_by_value("Next").first.click()

            b.choose("circumstances", "training")
            b.fill("description", "TIE Fighter piloting, level 1")
            b.select("date_month", "%s" % month)
            b.select("date_year", "%s" % (year - 2))
            b.find_by_value("Next").first.click()

            b.choose("circumstances", "part_time")
            b.fill("description", "Security guard, the Hutt")
            b.select("date_month", "%s" % month)
            b.select("date_year", "%s" % (year - 3))
            b.find_by_value("Next").first.click()

            self.assertTrue(b.is_text_present("Timeline"))
            self.assertTrue(b.is_text_present("Stormtrooper, Galactic Empire"))
            self.assertTrue(b.is_text_present("TIE Fighter piloting, level 1"))
            self.assertTrue(b.is_text_present("Security guard, the Hutt"))
            self.assertTrue(b.find_by_css(".exp-timeline"))

            b.fill("email", "test@example.org")
            b.find_by_value("Send").first.click()
            self.assertTrue(
                b.is_text_present(
                    "Your report has been sent to test@example.org")
            )
            self.assertEqual(len(mail.outbox), 1)
