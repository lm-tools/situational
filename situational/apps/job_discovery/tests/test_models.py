from situational.testing import BaseCase
from job_discovery import models


class TestJobDiscoveryModel(BaseCase):

    def setUp(self):
        self.report = models.JobDiscoveryReport.objects.create(
            postcode="N87RW"
        )
        self.other_report = models.JobDiscoveryReport.objects.create(
            postcode="N87RQ"
        )
        self.location = models.JobLocationToPostcode.objects.create(
            postcode="N87RW",
            location="location"
        )
        self.other_location = models.JobLocationToPostcode.objects.create(
            postcode="N87RQ",
            location="other_location"
        )
        self.job = models.Job.objects.create(
            location="location"
        )
        self.other_job = models.Job.objects.create(
            location="other_location"
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
