from base64 import b64decode
from io import BytesIO

from django.core.files import File
from django.test import TestCase

from report.models import Report
from travel_times.models import TravelTimesMap


class ReportBuilderMixin():
    def _dummy_travel_times_map(self):
        travel_times_map, created = TravelTimesMap.objects.get_or_create(
            postcode='SW1A 1AA',
            height=1200,
            width=1200,
        )
        if not travel_times_map.has_image:
            travel_times_map.image.save(
                'dummy_file.gif',
                File(BytesIO(
                    b64decode("R0lGODlhAQABAAAAACH5BAEAAAAALAAAAAABAAEAAAI=")
                ))
            )
        return travel_times_map

    def _populated_report(self, without=[]):
        populated_fields = {
            'postcode': 'SW1A 1AA',
            'location_json': '{"wgs84_lon": -0.141, "wgs84_lat": 51.501}',
            'top_categories': '[{"category": "Testing Jobs", "count": 165}]',
            'top_companies': '[{"company_name": "The Test Group"}]',
            'latest_jobs': '[{"company_name": "The Test Kitchen"}]',
            'travel_times_map': self._dummy_travel_times_map(),
        }
        for field in without:
            del populated_fields[field]
        return Report(**populated_fields)


class TestReportModel(TestCase):
    def test_population(self):
        r = Report(postcode='SW1A 1AA')
        r.save()
        r.populate_async()  # celery runs tasks synchronously for tests
        r.refresh_from_db()
        self.assertTrue(r.is_populated)


class TestReportIsPopulated(ReportBuilderMixin, TestCase):
    def test_new_reports_are_considered_unpopulated(self):
        self.assertFalse(Report().is_populated)

    def test_reports_with_all_fields_present_are_considered_populated(self):
        self.assertTrue(self._populated_report().is_populated)

    def test_reports_with_missing_fields_are_considered_unpopulated(self):
        for field in (Report.RESULT_FIELDS):
            with self.subTest(field=field):
                report = self._populated_report(without=[field])
                self.assertFalse(report.is_populated)

    def test_reports_without_travel_images_are_considered_unpopulated(self):
        report = self._populated_report()
        report.travel_times_map.image = None
        self.assertFalse(report.is_populated)


class TestReportPopulatedResultFields(ReportBuilderMixin, TestCase):
    def test_all_result_fields_populated(self):
        report = self._populated_report()
        self.assertCountEqual(
            report.populated_result_fields, Report.RESULT_FIELDS
        )

    def test_each_result_field_not_populated(self):
        for field in Report.RESULT_FIELDS:
            with self.subTest(field=field):
                report = self._populated_report(without=[field])
                self.assertNotIn(field, report.populated_result_fields)
