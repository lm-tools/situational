import uuid
from unittest.mock import patch, MagicMock

from django.core import mail
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
        job = models.Job.objects.create(adzuna_id=uuid.uuid4())
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


class TestReportView(BaseCase):

    def setUp(self):
        self.location = models.JobLocation.objects.create(
            adzuna_locations="Uk,London,Central London"
        )
        self.report = models.JobDiscoveryReport.objects.create(
            postcode="N87RW",
            location=self.location,
        )
        self.job_liked = models.Job.objects.create(adzuna_id=uuid.uuid4())
        self.job_liked_2 = models.Job.objects.create(adzuna_id=uuid.uuid4())
        self.job_disliked = models.Job.objects.create(adzuna_id=uuid.uuid4())
        self.location.jobs.add(self.job_liked)
        self.location.jobs.add(self.job_liked_2)
        self.location.jobs.add(self.job_disliked)

    def _report_url(self):
        return reverse("job_discovery:report",
                       kwargs={"guid": self.report.guid})

    def test_get_renders_no_jobs_if_no_jobs_seen(self):
        response = self.client.get(self._report_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_discovery/report.html")
        self.assertEqual(list(response.context["jobs"]), [])
        self.assertContains(response, "You have not liked any jobs so far.")

    def test_get_renders_jobs_liked(self):
        self.report.add_reaction(self.job_liked, "yes")
        self.report.add_reaction(self.job_liked_2, "yes")
        self.report.add_reaction(self.job_disliked, "no")
        response = self.client.get(self._report_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "job_discovery/report.html")
        self.assertEqual(
            list(response.context["jobs"]),
            [self.job_liked, self.job_liked_2]
        )


class TestSendView(BaseCase):
    def setUp(self):
        self.location = models.JobLocation.objects.create(
            adzuna_locations="Uk,London,Central London"
        )
        self.report = models.JobDiscoveryReport.objects.create(
            postcode="N87RW",
            location=self.location,
        )
        self.job_liked = models.Job.objects.create(adzuna_id=uuid.uuid4)
        self.location.jobs.add(self.job_liked)
        with patch("template_to_pdf.convertors.PrinceXML.convert") as convert:
            convert.return_value = "pdf-file-contents"
            self.response = self.client.post(
                reverse(
                    "job_discovery:send",
                    kwargs={'guid': self.report.guid}
                ),
                data={'email': 'test@example.org'},
            )

    def test_post_renders_correctly(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'job_discovery/send.html')

    def test_post_emails_the_histoy_report(self):
            self.assertEqual(len(mail.outbox), 1, "Mail should have been sent")
            message = mail.outbox[0]

            self.assertIn('test@example.org', message.to)
            self.assertEqual(len(message.attachments), 1)
            self.assertIn("Your job discovery report", message.body)
            self.assertIn(
                "Your job discovery report",
                message.alternatives[0][0]
            )
            self.assertEqual(message.attachments[0][1], "pdf-file-contents")
            self.assertEqual(message.attachments[0][2], 'application/pdf')
