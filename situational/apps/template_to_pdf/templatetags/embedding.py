import base64
import mimetypes
import subprocess

from django import template
from django.contrib.staticfiles.finders import find
from django.db import models

register = template.Library()


def _dataurl(f, mimetype):
    return "data:{};base64,{}".format(
        mimetype,
        str(base64.b64encode(f.read()), 'utf-8')
    )


def _dataurl_from_field_file(image_field_file, mimetype):
    if not mimetype:
        mimetype, _ = mimetypes.guess_type(image_field_file.name)
    f = image_field_file.file
    try:
        f.open()
        return _dataurl(f.file, mimetype)
    finally:
        f.file.close()


def _dataurl_from_path(image_path, mimetype):
    image_full_path = find(image_path)
    if not mimetype:
        mimetype, _ = mimetypes.guess_type(image_full_path)
    with open(image_full_path, 'rb') as f:
        return _dataurl(f, mimetype)


@register.simple_tag
def dataurl(image_path_or_field, mimetype=None):
    if isinstance(image_path_or_field, models.fields.files.ImageFieldFile):
        return _dataurl_from_field_file(image_path_or_field, mimetype)
    else:
        return _dataurl_from_path(image_path_or_field, mimetype)


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
