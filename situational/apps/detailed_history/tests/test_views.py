from unittest.mock import patch

from django.core import mail
from django.core.urlresolvers import reverse

from situational.testing import BaseCase


class TestSendView(BaseCase):
    def setUp(self):
        with patch("template_to_pdf.convertors.PrinceXML.convert") as convert:
            convert.return_value = "pdf-file-contents"
            self.response = self.client.post(
                reverse("detailed_history:send"),
                data={'email': 'test@example.org'},
            )

    def test_post_renders_correctly(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'detailed_history/send.html')

    def test_post_emails_the_histoy_report(self):
            self.assertEqual(len(mail.outbox), 1, "Mail should have been sent")
            message = mail.outbox[0]

            self.assertIn('test@example.org', message.to)
            self.assertEqual(len(message.attachments), 1)
            self.assertIn("Your history report", message.body)
            self.assertIn("Your history report", message.alternatives[0][0])
            self.assertEqual(message.attachments[0][1], "pdf-file-contents")
            self.assertEqual(message.attachments[0][2], 'application/pdf')
