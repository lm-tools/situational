from django import forms
from django.forms.forms import BoundField

from .helpers import LMIForAllClient
from .fields import MultiCharField


class FieldSet(object):
    """
    Taken from stackoverflow.com/questions/10366745/django-form-field-grouping

    Helper class to group BoundField objects together.
    """
    def __init__(self, form, fields, legend='', cls=None):
        self.form = form
        self.legend = legend
        self.fields = fields
        self.cls = cls

    def __iter__(self):
        for name in self.fields:
            field = self.form.fields[name]
            yield BoundField(self.form, field, name)


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

    sector = MultiCharField(
        count=SECTOR_INPUT_COUNT,
        label="How would you describe the types of jobs you could do?",
        help_text=" eg customer services, security, data entry, driver",
        require_all_fields=False,
        error_messages={'required': 'Enter at least one job role', },
    )


class JobDescriptionsForm(BaseLMIForm):
    def __init__(self, *args, **kwargs):
        keywords = kwargs['keywords']
        self.show_more = kwargs.get('show_more', [])
        del kwargs['keywords']
        if 'show_more' in kwargs:
            del kwargs['show_more']
        super().__init__(*args, **kwargs)
        self.fieldsets = []
        self._add_fields_from_keywords(keywords)

    def _add_fields_from_keywords(self, keywords):
        for keyword in keywords:
            if keyword:
                soc_codes = set()
                lmi_data = self.lmi_client.keyword_search(keyword)
                count = 3
                if keyword in self.show_more:
                    count = 6
                for item in lmi_data[:count]:
                    soc_code = str(item['soc'])
                    soc_codes.add(soc_code)
                    field = forms.BooleanField(
                        widget=forms.CheckboxInput,
                        label=item['title'],
                        help_text=item['description'],
                        required=False,
                    )
                    self.fields[soc_code] = field
                self.fieldsets.append(FieldSet(
                    self, list(soc_codes), keyword))

    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data.values()):
            raise forms.ValidationError(
                "Please select at least one job title",
                code='invalid'
            )
        return cleaned_data
