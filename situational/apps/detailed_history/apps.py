from django.apps import AppConfig


class DetailedHistoryConfig(AppConfig):
    name = 'detailed_history'
    verbose_name = "History (detailed)"
    icon_url = 'images/icons/app-icon-fuschia.png'
    start_url_name = "start"
    manifest = True
