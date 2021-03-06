from localflavor.gb.forms import GBPostcodeField

from django import forms

from . import widgets


class PostcodeForm(forms.Form):
    postcode = GBPostcodeField(
        widget=forms.TextInput(
            attrs={"class": "form-control form-control-1-4"})
    )


class SuggestionForm(forms.Form):
    RESPONSE_CHOICES = (
        ("no", "No, this isn't for me"),
        ("yes", "Yes, this sounds interesting"),
    )

    job_id = forms.CharField(widget=forms.HiddenInput)
    response = forms.ChoiceField(choices=RESPONSE_CHOICES,
                                 widget=widgets.MultipleSubmitButton,
                                 label="")
