import base64
import subprocess

from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import find

register = template.Library()


def b64encode_file(file):
    return base64.b64encode(file.read())

register.filter('b64encode_file', b64encode_file)


class StylesheetNotFoundException(Exception):
    pass


@register.simple_tag
def embed_stylesheet(filename):
    path = find(filename)
    if path:
        if path.endswith('.scss'):
            css = subprocess.check_output(["sass", path],
                                          universal_newlines=True)
        else:
            with open(path) as f:
                css = f.read()
        return "<style>\n{}\n</style>".format(css)
    else:
        raise StylesheetNotFoundException("Could not find {}".format(filename))
