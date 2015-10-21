from django.core.urlresolvers import reverse
from django.core import mail

from splinter import Browser

from situational.testing import BaseCase


class TestJobDiscovery(BaseCase):
    def test_happy_path(self):
        with Browser("django") as b:
            b.visit(reverse("job_discovery:start"))
            b.fill("postcode", "SW1A 1AA")
            b.find_by_text("Start").first.click()

            yes_jobs = []
            no_jobs = []

            for _ in range(5):
                no_jobs.append(b.find_by_css(".t-job-title").first.text)
                b.find_by_value("no").first.click()

            for _ in range(5):
                yes_jobs.append(b.find_by_css(".t-job-title").first.text)
                b.find_by_value("yes").first.click()

            # can't find by text as xpath hates apostrophes
            b.find_by_css(".t-done").first.click()

            for job in yes_jobs:
                self.assertTrue(
                    b.is_text_present(job))

            for job in no_jobs:
                self.assertTrue(
                    b.is_text_not_present(job))

            b.fill("email", "test@example.org")
            b.find_by_value("Send").first.click()
            self.assertTrue(
                b.is_text_present(
                    "Sent to test@example.org")
            )
            self.assertEqual(len(mail.outbox), 1)
