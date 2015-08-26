from django.apps import AppConfig


class QuickHistoryConfig(AppConfig):
    name = 'quick_history'
    verbose_name = "Quick: Tell your work coach your history"
    icon_url = 'images/icons/app-icon-blue.png'
    start_url_name = "start"
    manifest = True
