from django.apps import AppConfig


class SectorsConfig(AppConfig):
    name = 'sectors'
    verbose_name = "Job roles"
    icon_url = 'images/icons/app-icon-red.png'
    start_url_name = "start"
    manifest = True
