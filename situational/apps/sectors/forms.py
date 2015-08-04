import json

from django import forms

from localflavor.gb.forms import GBPostcodeField


class NoColonForm(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


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


class SectorForm(NoColonForm):
    SECTOR_INPUT_COUNT = 3

    postcode = GBPostcodeField()
    sector = forms.CharField(
        widget=SectorSelectorWidget(SECTOR_INPUT_COUNT),
        label="Job roles eg security, data entry, driver",
    )
