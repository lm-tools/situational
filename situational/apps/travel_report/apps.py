from django.apps import AppConfig


class TravelReportConfig(AppConfig):
    name = 'travel_report'
    verbose_name = "Understand where you could travel for work"
    icon_url = 'images/icons/app-icon-yellow.png'
    start_url_name = "start"
    manifest = True
