from base64 import b64decode
from io import BytesIO

from django.core.files import File
from django.test import TestCase

from report.models import Report
from travel_times.models import TravelTimesMap


class TestReportModel(TestCase):
    def test_population(self):
        r = Report(postcode='SW1A 1AA')
        r.save()
        r.populate_async()  # celery runs tasks synchronously for tests
        r.refresh_from_db()
        self.assertTrue(r.is_populated)


class TestReportIsPopulated(TestCase):
    def _populated_report(self):
        dummy_travel_times_map = TravelTimesMap(
            postcode='SW1A 1AA',
            height=1200,
            width=1200
        )
        dummy_travel_times_map.image.save(
            'dummy_file.gif',
            File(BytesIO(
                b64decode("R0lGODlhAQABAAAAACH5BAEAAAAALAAAAAABAAEAAAI=")
            )),
            False,
        )
        dummy_travel_times_map.save()

        return Report(
            postcode='SW1A 1AA',
            place_name='Covent Garden',
            location_json='{"wgs84_lon": -0.141, "wgs84_lat": 51.501}',
            top_categories='[{"category": "Testing Jobs", "count": 165}]',
            top_companies='[{"company_name": "The Test Group"}]',
            latest_jobs='[{"company_name": "The Test Kitchen"}]',
            travel_times_map=dummy_travel_times_map,
        )

    def _populated_report_without(self, field, blank_value=''):
        report = self._populated_report()
        setattr(report, field, blank_value)
        return report

    def test_new_reports_are_considered_unpopulated(self):
        self.assertFalse(Report().is_populated)

    def test_reports_with_all_contents_present_are_considered_populated(self):
        self.assertTrue(self._populated_report().is_populated)

    def test_reports_without_place_name_are_considered_unpopulated(self):
        self.assertFalse(
            self._populated_report_without('place_name').is_populated
        )

    def test_reports_without_location_json_are_considered_unpopulated(self):
        self.assertFalse(
            self._populated_report_without('location_json').is_populated
        )

    def test_reports_without_top_categories_are_considered_unpopulated(self):
        self.assertFalse(
            self._populated_report_without('top_categories').is_populated
        )

    def test_reports_without_top_companies_are_considered_unpopulated(self):
        self.assertFalse(
            self._populated_report_without('top_companies').is_populated
        )

    def test_reports_without_latest_jobs_are_considered_unpopulated(self):
        self.assertFalse(
            self._populated_report_without('latest_jobs').is_populated
        )

    def test_reports_without_travel_times_map_are_considered_unpopulated(self):
        self.assertFalse(
            self._populated_report_without('travel_times_map', None)
                .is_populated
        )

    def test_reports_without_travel_images_are_considered_unpopulated(self):
        report = self._populated_report()
        report.travel_times_map.image = None
        self.assertFalse(report.is_populated)
