import base64
import mimetypes
import subprocess

from django import template
from django.conf import settings
from django.contrib.staticfiles.finders import find

register = template.Library()


@register.simple_tag
def dataurl(image_field, mimetype=None):
    if not mimetype:
        mimetype, _ = mimetypes.guess_type(image_field.name)
    f = image_field.file
    try:
        f.open()
        return "data:{};base64,{}".format(
            mimetype,
            str(base64.b64encode(f.read()), 'utf-8')
        )
    finally:
        f.close()


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
