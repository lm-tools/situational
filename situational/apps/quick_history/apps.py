from django.apps import AppConfig


class QuickHistoryConfig(AppConfig):
    name = 'quick_history'
    verbose_name = "History snapshot"
    icon_url = 'images/icons/app-icon-blue.png'
    start_url_name = "start"
    manifest = True
