import uuid

from situational.testing import BaseCase
from job_discovery import models


class TestJobDiscoveryModel(BaseCase):

    def setUp(self):
        self.location = models.JobLocation.objects.create(
            adzuna_locations="location"
        )
        self.other_location = models.JobLocation.objects.create(
            adzuna_locations="other_location"
        )
        self.report = models.JobDiscoveryReport.objects.create(
            postcode="N87RW",
            location=self.location
        )
        self.other_report = models.JobDiscoveryReport.objects.create(
            postcode="N87RQ",
            location=self.other_location
        )
        self.job = models.Job.objects.create(adzuna_id=uuid.uuid4())
        self.job_2 = models.Job.objects.create(adzuna_id=uuid.uuid4())
        self.location.jobs.add(self.job, self.job_2)
        self.other_job = models.Job.objects.create(adzuna_id=uuid.uuid4())
        self.other_location.jobs.add(self.other_job)

    def test_get_suggestion_returns_job_from_correct_location(self):
        suggestion = self.report.get_suggestion()
        other_suggestion = self.other_report.get_suggestion()
        self.assertIn(
            suggestion,
            [self.job, self.job_2]
        )
        self.assertEqual(
            other_suggestion,
            self.other_job
        )

    def test_get_suggestion_returns_job_not_already_seen(self):
        models.Reaction.objects.create(
            job=self.job,
            report=self.report
        )
        suggestion = self.report.get_suggestion()
        self.assertEqual(
            suggestion,
            self.job_2
        )

    def test_get_suggestion_imports_jobs_if_needed(self):
        no_jobs_location = models.JobLocation.objects.create(
            adzuna_locations="UK,London,Central London"
        )
        report = models.JobDiscoveryReport.objects.create(
            postcode="N87RZ",
            location=no_jobs_location
        )
        report.get_suggestion()
        number_jobs = no_jobs_location.jobs.count()
        self.assertTrue(number_jobs, 50)
