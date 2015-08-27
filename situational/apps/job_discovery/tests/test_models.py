from situational.testing import BaseCase
from job_discovery import models


class TestJobDiscoveryModel(BaseCase):

    def setUp(self):
        self.location = models.JobLocation.objects.create(
            postcode="N87RW",
            adzuna_locations="location"
        )
        self.other_location = models.JobLocation.objects.create(
            postcode="N87RQ",
            adzuna_locations="other_location"
        )
        self.report = models.JobDiscoveryReport.objects.create(
            location=self.location
        )
        self.other_report = models.JobDiscoveryReport.objects.create(
            location=self.other_location
        )
        self.job = models.Job.objects.create(
            location=self.location
        )
        self.job_2 = models.Job.objects.create(
            location=self.location
        )
        self.other_job = models.Job.objects.create(
            location=self.other_location
        )

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

    def test_get_suggestion_returns_random_job(self):
        job_1_returned = 0
        job_2_returned = 0
        for x in range(500):
            suggestion = self.report.get_suggestion()
            if suggestion == self.job:
                job_1_returned += 1
            else:
                job_2_returned += 1
        self.assertTrue(225 <= job_1_returned <= 275)
        self.assertTrue(225 <= job_2_returned <= 275)

    def test_get_suggestion_imports_jobs_if_needed(self):
        no_jobs_location = models.JobLocation.objects.create(
            postcode="N87RZ",
            adzuna_locations="UK,London,Central London"
        )
        report = models.JobDiscoveryReport.objects.create(
            location=no_jobs_location
        )
        report.get_suggestion()
        number_jobs = models.Job.objects.filter(
            location=no_jobs_location
        ).count()
        self.assertTrue(number_jobs, 50)
