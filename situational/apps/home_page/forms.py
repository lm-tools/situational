from django import forms


class FeedbackForm(forms.Form):
    name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    subject = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    message = forms.CharField(
        required=True, widget=forms.Textarea(attrs={"class": "form-control"})
    )
