from django.conf import settings
from django.core.urlresolvers import resolve


def govuk_frontend_settings(request):
    return {
        'homepage_url': getattr(settings, 'GOVUK_HOMEPAGE_URL'),
        'logo_link_title': getattr(settings, 'GOVUK_LOGO_LINK_TITLE'),
    }


def get_current_path(request):
    return {
        'current_path': request.get_full_path(),
    }


def get_current_namespace(request):
    r = resolve(request.path)
    return {
        'namespace': r.namespace,
    }


def google_analytics(request):
    return {
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID'),
    }
