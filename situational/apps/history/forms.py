from django import forms


class HistoryDetailsForm(forms.Form):
    CIRCUMSTANCE_CHOICES = [
        ("full_time", "Full time"),
        ("part_time", "Part time"),
        ("work_programme", "Work programme"),
        ("sick", "Sick"),
        ("caring", "Caring"),
        ("children", "Children"),
        ("education", "Education"),
        ("unemployed", "Unemployed"),
        ("other", "Other"),
    ]
    DURATION_CHOICES = [
        ('less_than_1', 'less than 1 month'),
        ('1_to_3', '1 to 3 months'),
        ('3_to_6', '3 to 6 months'),
        ('6_to_9', '6 to 9 months'),
        ('9_to_12', '9 to 12 months'),
        ('12_to_18', '12 to 18 months'),
        ('18_to_24', '18 to 24 months'),
        ('over_24', 'over 24 months')
    ]
    circumstances = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CIRCUMSTANCE_CHOICES
    )
    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        widget=forms.RadioSelect())
    other_more = forms.CharField(required=False)
    description = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(HistoryDetailsForm, self).clean()
        circumstances = cleaned_data.get("circumstances")
        other_more = cleaned_data.get("other_more")
        if circumstances and "other" in circumstances and not other_more:
            description_missing = "Please enter a short description for other"
            self.add_error('circumstances', description_missing)
        return cleaned_data
