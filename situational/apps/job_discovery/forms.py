from localflavor.gb.forms import GBPostcodeField

from django import forms

from . import widgets


class PostcodeForm(forms.Form):
    postcode = GBPostcodeField()


class SuggestionForm(forms.Form):
    RESPONSE_CHOICES = (
        ("yes", "Yes"),
        ("no", "No"),
    )

    job_id = forms.CharField(widget=forms.HiddenInput)
    response = forms.ChoiceField(choices=RESPONSE_CHOICES,
                                 widget=widgets.MultipleSubmitButton)
