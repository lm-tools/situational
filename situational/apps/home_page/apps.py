from django.apps import AppConfig


class HomePageConfig(AppConfig):
    name = 'home_page'
    verbose_name = "Labour market tools"
    icon_url = 'images/icons/app-icon-green.png'
    start_url_name = "home"
    manifest = True
