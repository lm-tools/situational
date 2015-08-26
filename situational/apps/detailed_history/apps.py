from django.apps import AppConfig


class DetailedHistoryConfig(AppConfig):
    name = 'detailed_history'
    verbose_name = "Tell your work coach your history"
    icon_url = 'images/icons/app-icon-fuschia.png'
    start_url_name = "start"
    manifest = True
