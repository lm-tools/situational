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
        self.assertEqual(
            suggestion,
            self.job
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
