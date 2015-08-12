from django.core import mail
from django.test import TestCase

from templated_email import send_templated_email


class TestSendTemplatedEmail(TestCase):

    def test_sends_multipart_email_with_attachments(self):
        send_templated_email(
            template_name='templated_email/test_fixture',
            context={'foo': 'bar'},
            to=['hello@example.org'],
            subject='Testing templated email',
            attachments=[('test.txt', 'file contents', 'text/plain')]
        )

        self.assertEqual(len(mail.outbox), 1)  # sanity check
        message = mail.outbox[0]

        with self.subTest('to'):
            self.assertEqual(message.to, ['hello@example.org'])

        with self.subTest('subject'):
            self.assertEqual(message.subject, 'Testing templated email')

        with self.subTest('attachments'):
            self.assertEqual(message.attachments,
                             [('test.txt', 'file contents', 'text/plain')])

        with self.subTest('plain text body'):
            self.assertEqual(message.body, "Hi, foo was 'bar'.\n")
            self.assertEqual(message.content_subtype, 'plain')

        with self.subTest('html body'):
            self.assertEqual(len(message.alternatives), 1)  # sanity check
            html_body, html_subtype = message.alternatives[0]
            self.assertEqual(html_body,
                             "<p>Hi, foo was <strong>bar</strong>.</p>\n")
            self.assertEqual(html_subtype, 'text/html')
