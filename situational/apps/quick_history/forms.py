from django import forms
from . import widgets


class HistoryDetailsForm(forms.Form):

    CIRCUMSTANCE_CHOICES = [
        ("full_time", "Full time"),
        ("part_time", "Part time"),
        ("work_programme", "Work programme"),
        ("unemployed", "Unemployed"),
        ("sick", "Off sick"),
        ("training", "In full time training"),
        ("caring", "Caring full time for others"),
        ("none", "None of these"),
    ]
    circumstances = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=CIRCUMSTANCE_CHOICES
    )
    date = forms.DateField(
        widget=widgets.MonthYearWidget(years=range(1960, 2016))
    )
    description = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(HistoryDetailsForm, self).clean()
        # TODO: check date is <= last_known_start_date
        return cleaned_data
