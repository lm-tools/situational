from django.conf import settings


def govuk_frontend_settings(request):
    return {
        'homepage_url': getattr(settings, 'GOVUK_HOMEPAGE_URL'),
        'logo_link_title': getattr(settings, 'GOVUK_LOGO_LINK_TITLE'),
    }
