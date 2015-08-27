from unittest.mock import patch, MagicMock

from django.core.urlresolvers import reverse

from situational.testing import BaseCase
from job_discovery import models

class TestStartView(BaseCase):

    def test_post(self):
        response = self.client.post(
            reverse("job_discovery:start"),
            {"postcode": "N87RW"}
        )
        last_report = models.JobDiscoveryReport.objects.get()
        with self.subTest("creates an empty report"):
            self.assertEqual(
                last_report.postcode,
                "N87RW"
            )

        with self.subTest("redirects to job discovery suggestion"):
            self.assertRedirects(
                response,
                reverse("job_discovery:suggestion",
                        kwargs={"guid":last_report.guid})
            )

    def test_get_renders_start_page(self):
        response = self.client.get(reverse("job_discovery:start"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_discovery/start.html")


class TestSuggestionView(BaseCase):

    def setUp(self):
        self.report = models.JobDiscoveryReport.objects.create(
            postcode="N87RW",
        )

    def test_get_renders_job_suggestion(self):
        with patch('job_discovery.models.JobDiscoveryReport.get_suggestion') \
                   as get_suggestion:
            job = MagicMock()
            get_suggestion.return_value = job

            response = self.client.get(
                reverse("job_discovery:suggestion",
                        kwargs={"guid":self.report.guid})
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "job_discovery/suggestion.html")
            self.assertEqual(response.context["job"], job)
