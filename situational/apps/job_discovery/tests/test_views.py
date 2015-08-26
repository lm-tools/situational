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
        latest_report = models.JobDiscoveryReport.objects.get()
        latest_location = models.JobLocation.objects.get()

        with self.subTest("creates a JobLocation with locations from Adzuna "
                          "based on the postcode"):
            self.assertEqual(
                latest_location.adzuna_locations,
                "UK,London,North London"
            )

        with self.subTest("creates an empty report, for the postcode and "
                          "job location"):
            self.assertEqual(latest_report.postcode, "N87RW")
            self.assertEqual(latest_report.location, latest_location)

        with self.subTest("redirects to job discovery suggestion"):
            self.assertRedirects(
                response,
                reverse("job_discovery:suggestion",
                        kwargs={"guid": latest_report.guid})
            )

    def test_get_renders_start_page(self):
        response = self.client.get(reverse("job_discovery:start"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_discovery/start.html")


class TestSuggestionView(BaseCase):

    def setUp(self):
        self.location = models.JobLocation.objects.create(
            adzuna_locations="Uk,London,Central London"
        )
        self.report = models.JobDiscoveryReport.objects.create(
            postcode="N87RW",
            location=self.location,
        )

    def _suggestion_url(self):
        return reverse("job_discovery:suggestion",
                       kwargs={"guid": self.report.guid})

    def test_get_renders_job_suggestion(self):
        with patch('job_discovery.models.JobDiscoveryReport.get_suggestion') \
                as get_suggestion:
            job = MagicMock()
            get_suggestion.return_value = job

            response = self.client.get(self._suggestion_url())

            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "job_discovery/suggestion.html")
            self.assertEqual(response.context["job"], job)

    def test_post(self):
        job = models.Job.objects.create(adzuna_id="foo")
        job_response = "yes"

        response = self.client.post(
            self._suggestion_url(),
            data={"job_id": job.id, "response": job_response},
        )

        with self.subTest("adds a job reaction to the report"):
            self.report.refresh_from_db()
            self.assertIn(job, self.report.seen_jobs.all())
            reactions = self.report.reactions.filter(job=job,
                                                     response=job_response)
            self.assertEqual(len(reactions), 1,
                             "Report should contain expected reaction")

        with self.subTest("redirects to new suggestion"):
            self.assertRedirects(response, self._suggestion_url())
