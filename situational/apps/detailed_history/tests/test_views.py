from django.core.urlresolvers import reverse

from situational.testing import BaseCase


class TestSendView(BaseCase):
    def test_post_renders_correctly(self):
        response = self.client.post(reverse("detailed_history:send"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detailed_history/send.html')
