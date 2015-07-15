from django import forms

from localflavor.gb.forms import GBPostcodeField


class PostcodeForm(forms.Form):
    postcode = GBPostcodeField()
