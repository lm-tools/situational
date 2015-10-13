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


class EmailForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': 'Please provide an email address.',
            'invalid': 'Please provide a valid email address.'
        },
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
