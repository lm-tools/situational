from django.test import TestCase

from report.models import Report


class TestReportModel(TestCase):
    def test_get_item(self):
        r = Report(postcode='SW1A 1AA')
        r.save()
        # r['location'] = "foo"
        r.populate_async()
        self.assertTrue(r.is_populated)
