from django import forms

YES_NO_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No')
]


class OneTextFieldForm(forms.Form):
    text = forms.CharField(required=False, widget=forms.Textarea)


class CurrentWorkStatusForm(forms.Form):
    WORK_STATUS_CHOICES = [
        ('full_time', 'Full time'),
        ('part_time', 'Part time'),
        ('unemployed', 'Unemployed'),
        ('off_sick', 'Off sick'),
        ('work_programme', 'Work programme')
    ]
    status = forms.ChoiceField(
        choices=WORK_STATUS_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    description = forms.CharField(required=False, widget=forms.Textarea)


class PreviousYearsForm(forms.Form):
    changes = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    description = forms.CharField(required=False, widget=forms.Textarea)


class TrainingEducationForm(forms.Form):
    yes_or_no = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect(),
        required=False
    )
    current = forms.CharField(required=False, widget=forms.Textarea)
    previous = forms.CharField(required=False, widget=forms.Textarea)
