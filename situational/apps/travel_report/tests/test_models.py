from base64 import b64decode
from io import BytesIO
from unittest.mock import patch

from django.core import mail
from django.core.files import File

from travel_report.models import TravelReport
from travel_times.models import TravelTimesMap
from situational.testing import BaseCase


class TravelReportBuilderMixin():
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
            'travel_times_map': self._dummy_travel_times_map(),
        }
        for field in without:
            del populated_fields[field]
        return TravelReport(**populated_fields)


class TestTravelReportModel(BaseCase):
    def test_population(self):
        r = TravelReport(postcode='SW1A 1AA')
        r.save()
        r.populate_async()  # celery runs tasks synchronously for tests
        r.refresh_from_db()
        self.assertTrue(r.is_populated)


class TestTravelReportIsPopulated(TravelReportBuilderMixin, BaseCase):
    def test_new_reports_are_considered_unpopulated(self):
        self.assertFalse(TravelReport().is_populated)

    def test_reports_with_all_fields_present_are_considered_populated(self):
        self.assertTrue(self._populated_report().is_populated)

    def test_reports_with_missing_fields_are_considered_unpopulated(self):
        for field in (TravelReport.RESULT_FIELDS):
            with self.subTest(field=field):
                report = self._populated_report(without=[field])
                self.assertFalse(report.is_populated)

    def test_reports_without_travel_images_are_considered_unpopulated(self):
        report = self._populated_report()
        report.travel_times_map.image = None
        self.assertFalse(report.is_populated)


class TestTravelReportPopulatedResultFields(TravelReportBuilderMixin,
                                            BaseCase):
    def test_all_result_fields_populated(self):
        report = self._populated_report()
        self.assertCountEqual(
            report.populated_result_fields, TravelReport.RESULT_FIELDS
        )

    def test_each_result_field_not_populated(self):
        for field in TravelReport.RESULT_FIELDS:
            with self.subTest(field=field):
                report = self._populated_report(without=[field])
                self.assertNotIn(field, report.populated_result_fields)


class TestTravelReportSendTo(TravelReportBuilderMixin, BaseCase):
    def test_send_pdf_to_eprovided_mail_address(self):
        report = self._populated_report()
        with patch.object(report, 'to_pdf') as to_pdf_mock:
            to_pdf_mock.return_value = 'mock pdf content'
            report.send_to('test-address@example.org')

        self.assertEqual(len(mail.outbox), 1)  # sanity check
        message = mail.outbox[0]

        self.assertIn('test-address@example.org', message.to)
        self.assertEqual(len(message.attachments), 1)
        self.assertIn(
            "Your travel time map report for {}".format(report.postcode),
            message.body,
        )
        self.assertIn(
            "Your travel time map report for {}".format(report.postcode),
            message.alternatives[0][0],
        )
        self.assertEqual(message.attachments[0][1], 'mock pdf content')
        self.assertEqual(message.attachments[0][2], 'application/pdf')
