from django.apps import apps
from django.core.urlresolvers import reverse

from situational.testing import BaseCase


class TestManifestView(BaseCase):
    def test_all_apps(self):
        base_url = reverse('home_page:manifest')

        for app_name in apps.app_configs:
            req = self.client.get(base_url, {'app': app_name})
            self.assertEqual(req.status_code, 200)
