import six

from django import template


def replace_underscores(value, replacement=" "):
    if isinstance(value, six.string_types):
        return value.replace("_", replacement)
    else:
        return value

register = template.Library()
register.filter('replace_underscores', replace_underscores)
