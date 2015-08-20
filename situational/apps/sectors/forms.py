from django import forms

from localflavor.gb.forms import GBPostcodeField
from .helpers import LMIForAllClient
from .fields import MultiCharField


class NoColonForm(forms.Form):
    """
    Removes the default colons from form labels.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


class BaseLMIForm(NoColonForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lmi_client = LMIForAllClient()


class SectorForm(NoColonForm):
    SECTOR_INPUT_COUNT = 3

    postcode = GBPostcodeField(required=True, label="Your postcode")
    sector = MultiCharField(
        count=SECTOR_INPUT_COUNT,
        label="How would you describe the types of jobs you could do?"
              " (eg security, data entry, driver)",
        require_all_fields=False,
        error_messages={'required': 'Enter at least one job role', },
    )


class JobDescriptionsForm(BaseLMIForm):
    def __init__(self, *args, **kwargs):
        keywords = kwargs['keywords']
        del kwargs['keywords']
        super().__init__(*args, **kwargs)
        self._add_fields_from_keywords(keywords)

    def _add_fields_from_keywords(self, keywords):
        for keyword in keywords:
            if keyword:
                lmi_data = self.lmi_client.keyword_search(keyword)
                for item in lmi_data[:3]:
                    self.fields[item['soc']] = forms.BooleanField(
                        widget=forms.CheckboxInput,
                        label=item['title'],
                        help_text=item['description'],
                        required=False,
                    )

    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data.values()):
            raise forms.ValidationError(
                "Please select at least one job title",
                code='invalid'
            )
        return cleaned_data


class SOCCodesView(BaseLMIForm):
    def __init__(self, *args, **kwargs):
        soc_codes = kwargs['soc_codes']
        del kwargs['soc_codes']

        if 'postcode' not in kwargs:
            raise KeyError("postcode not provided")
        postcode = kwargs['postcode']
        del kwargs['postcode']

        super().__init__(*args, **kwargs)
        self._add_soc_code_data(soc_codes)
        self._add_resident_occupations(postcode)
        self._add_jobs_breakdown(postcode)

    def _add_soc_code_data(self, soc_codes):
        self.soc_data = {}
        for soc_code in soc_codes:
            self.soc_data[soc_code] = {
                'pay': self.lmi_client.pay(soc_code),
                'hours_worked': self.lmi_client.hours_worked(soc_code),
                'info': self.lmi_client.soc_code_info(soc_code),
            }

    def _add_resident_occupations(self, postcode):
        self.resident_occupations = \
            self.lmi_client.resident_occupations(postcode)

    def _add_jobs_breakdown(self, postcode):
        self.jobs_breakdown = \
            self.lmi_client.jobs_breakdown(postcode)
