from django.apps import AppConfig


class JobDiscoveryConfig(AppConfig):
    name = 'job_discovery'
    verbose_name = "Discover jobs"
    icon_url = 'images/icons/app-icon-turquoise.png'
    start_url_name = "start"
    manifest = True
