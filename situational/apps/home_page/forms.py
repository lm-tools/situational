from django import forms

TOOLS = [
    ('all', 'All the tools'),
    ('travel', 'Where you could travel for work'),
    ('sectors', 'Understand what sort of jobs you could do'),
    ('discovery', 'Discover jobs to apply for')
]
FEEDBACK_TYPES = [
    ('not_working', 'Something isn\'t working'),
    ('new_idea', 'I would like to suggest a new idea'),
    ('confusing_coach', 'I found something confusing'),
    ('confusing_claimant', 'A claimant found something confusing')
]


class FeedbackForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': 'Please provide your name.'
        },
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        error_messages={
            'required': 'Please provide an email address.',
            'invalid': 'Please provide a valid email address.'
        },
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    message = forms.CharField(
        error_messages={
            'required': 'Please provide more detail.'
        },
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control"})
    )
    tool = forms.ChoiceField(
        error_messages={
            'required': 'Please select one of the tools.'
        },
        choices=TOOLS,
        widget=forms.RadioSelect
    )
    feedback_type = forms.ChoiceField(
        error_messages={
            'required': 'Please select the kind of feedback you are providing.'
        },
        choices=FEEDBACK_TYPES,
        widget=forms.RadioSelect
    )


class EmailForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': 'Please provide an email address.',
            'invalid': 'Please provide a valid email address.'
        },
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
