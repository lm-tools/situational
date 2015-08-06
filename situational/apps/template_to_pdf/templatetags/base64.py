import base64

from django import template

register = template.Library()


def b64encode_file(file):
    return base64.b64encode(file.read())

register.filter('b64encode_file', b64encode_file)
