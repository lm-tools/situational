import json

from django import forms
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.forms.utils import flatatt
from django.utils.datastructures import MultiValueDict


class SectorSelectorWidget(forms.MultiWidget):
    def __init__(self, count, attrs=None):
        _widgets = []
        for w in range(count):
            _widgets.append(forms.TextInput(attrs=attrs))

        super().__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return json.loads(value)
        return []


class SectorForm(forms.Form):
    SECTOR_INPUT_COUNT = 3

    sector = forms.CharField(widget=SectorSelectorWidget(SECTOR_INPUT_COUNT))
