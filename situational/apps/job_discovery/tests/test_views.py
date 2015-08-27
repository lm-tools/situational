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
                last_report.location.postcode,
                "N87RW"
            )

        with self.subTest("redirects to job discovery suggestion"):
            self.assertRedirects(
                response,
                reverse("job_discovery:suggestion",
                        kwargs={"guid": last_report.guid})
            )

    def test_get_renders_start_page(self):
        response = self.client.get(reverse("job_discovery:start"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_discovery/start.html")


class TestSuggestionView(BaseCase):

    def setUp(self):
        location = models.JobLocation.objects.create(
            postcode="N87RW",
            adzuna_locations="locationstring"
        )
        self.report = models.JobDiscoveryReport.objects.create(
            location=location,
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

    def test_post_adds_a_job_reaction_to_the_report(self):
        location = models.JobLocation.objects.create(
            postcode="N87RW",
            adzuna_locations="location"
        )
        job = models.Job.objects.create(
            location=location
        )
        response = "yes"

        self.client.post(
            self._suggestion_url(),
            data={"job_id": job.id, "response": response},
        )

        self.report.refresh_from_db()
        self.assertIn(job, self.report.seen_jobs.all())
        reactions = self.report.reactions.filter(job=job, response=response)
        self.assertEqual(len(reactions), 1,
                         "Report should contain expected reaction")
