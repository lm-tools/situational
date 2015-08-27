from django import forms

from localflavor.gb.forms import GBPostcodeField


class PostcodeForm(forms.Form):
    postcode = GBPostcodeField()


class SuggestionForm(forms.Form):
    job_id = forms.CharField(widget=forms.HiddenInput)
    response = forms.CharField()
