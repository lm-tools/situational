import re

from django import template

register = template.Library()

heading_re = re.compile("n\.e\.c\.\s*$")
description_re = re.compile("not elsewhere classified in .*\.$")


def friendly_soc_title(text):
    return heading_re.sub('', text).strip()


def friendly_soc_description(text):
    return description_re.sub('', text).strip(". ") + "."

register.filter('friendly_soc_title', friendly_soc_title)
register.filter('friendly_soc_description', friendly_soc_description)
