from django.core import mail
from django.core.urlresolvers import reverse

from situational.testing import BaseCase


class TestHomePageView(BaseCase):
    def test_post_sends_feedback(self):
        response = self.client.post(
            reverse('home_page:home'),
            data={
                'name': 'Harry Potter',
                'email': 'test@example.org',
                'message': 'Your home page needs more animated gifs',
                'tool': 'all',
                'feedback_type': 'not_working',
            }
        )

        with self.subTest('redirects to the thank you page'):
            self.assertRedirects(response, reverse('home_page:thank_you'))

        with self.subTest('sends the feedback email'):
            self.assertEqual(len(mail.outbox), 1, 'Mail should have been sent')
            message = mail.outbox[0]
            self.assertIn('feedback@lm-tools.com', message.to)
            self.assertIn('Something isn\'t working', message.subject)
            self.assertIn('All the tools', message.subject)
            self.assertIn('Harry Potter', message.body)
            self.assertIn('test@example.org', message.body)
            self.assertIn('Your home page needs more animated gifs',
                          message.body)
            self.assertIn('Harry Potter', message.alternatives[0][0])
            self.assertIn('test@example.org', message.alternatives[0][0])
            self.assertIn('Your home page needs more animated gifs',
                          message.alternatives[0][0])
