from django.conf import settings


def govuk_frontend_settings(request):
    return {
        'homepage_url': getattr(settings, 'GOVUK_HOMEPAGE_URL'),
        'logo_link_title': getattr(settings, 'GOVUK_LOGO_LINK_TITLE'),
    }

def get_current_path(request):
    return {
       'current_path': request.get_full_path()
     }
