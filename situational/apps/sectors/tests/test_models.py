from base64 import b64decode
from io import BytesIO
from unittest.mock import patch

from django.core import mail
from django.core.files import File

from sectors.models import SectorsReport
from situational.testing import BaseCase


class SectorsReportBuilderMixin():

    SOC_TITLES = [
        'Construction and building trades supervisors',
        'Building and civil engineering technicians'
    ]

    def _populated_report(self, without=[]):
        populated_fields = {
            'postcode': 'SW1A 1AA',
            'soc_codes': '3114,5330',
            'jobs_breakdown': {},
            'resident_occupations': {},
            'soc_code_data': {
                '5330': {
                    'info': {
                        'title': self.SOC_TITLES[0]
                    }
                },
                '3114': {
                    'info': {
                        'title': self.SOC_TITLES[1]
                    }
                }
            }
        }
        for field in without:
            del populated_fields[field]
        return SectorsReport(**populated_fields)


class TestSectorsReportModel(BaseCase):
    def test_population(self):
        r = SectorsReport(postcode='SW1A 1AA', soc_codes='3114,5330')
        r.save()
        r.populate_async()  # celery runs tasks synchronously for tests
        r.refresh_from_db()
        self.assertTrue(r.is_populated)


class TestSectorsReportIsPopulated(SectorsReportBuilderMixin, BaseCase):
    def test_new_reports_are_considered_unpopulated(self):
        self.assertFalse(SectorsReport().is_populated)

    def test_reports_with_all_fields_present_are_considered_populated(self):
        self.assertTrue(self._populated_report().is_populated)

    def test_reports_with_missing_fields_are_considered_unpopulated(self):
        for field in (SectorsReport.RESULT_FIELDS):
            with self.subTest(field=field):
                report = self._populated_report(without=[field])
                self.assertFalse(report.is_populated)


class TestSectorsReportPopulatedFields(SectorsReportBuilderMixin, BaseCase):
    def test_all_result_fields_populated(self):
        report = self._populated_report()
        self.assertCountEqual(
            report.populated_result_fields, SectorsReport.RESULT_FIELDS
        )

    def test_each_result_field_not_populated(self):
        for field in SectorsReport.RESULT_FIELDS:
            with self.subTest(field=field):
                report = self._populated_report(without=[field])
                self.assertNotIn(field, report.populated_result_fields)


class TestSectorsReportSendTo(SectorsReportBuilderMixin, BaseCase):
    def test_send_pdf_to_eprovided_mail_address(self):
        report = self._populated_report()
        with patch.object(report, 'to_pdf') as to_pdf_mock:
            to_pdf_mock.return_value = 'mock pdf content'
            report.send_to('test-address@example.org')

        self.assertEqual(len(mail.outbox), 1)  # sanity check
        message = mail.outbox[0]

        self.assertIn('test-address@example.org', message.to)
        self.assertEqual(len(message.attachments), 1)
        self.assertIn("Your sectors report", message.body)
        self.assertIn("Your sectors report", message.alternatives[0][0])
        for soc_title in self.SOC_TITLES:
            self.assertIn(soc_title, message.body)
            self.assertIn(soc_title, message.alternatives[0][0])
        self.assertEqual(message.attachments[0][1], 'mock pdf content')
        self.assertEqual(message.attachments[0][2], 'application/pdf')
