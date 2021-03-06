# The following code was adapted from:
# https://djangosnippets.org/snippets/10522/
import datetime
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

__all__ = ('MonthYearWidget',)

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')


class MonthYearWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes for month and year,
    with 'day' defaulting to the first of the month.

    Based on SelectDateWidget, in

    django/trunk/django/forms/extras/widgets.py


    """
    none_value_month = (0, 'Month')
    none_value_year = (0, 'Year')
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years
        # to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = list(reversed(years))
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year, this_year + 10)

    def render(self, name, value, attrs=None):
        try:
            y_val, m_val = value.year, value.month
        except AttributeError:
            y_val = m_val = None
            if isinstance(value, str):
                match = RE_DATE.match(value)
                if match:
                    y_val, m_val, d_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = list(MONTHS.items())
        if not (self.required and value):
            month_choices.append(self.none_value_month)
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, m_val, local_attrs)
        output.append('<div class="date-select">' + select_html + '</div>')

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value_year)
        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, y_val, local_attrs)
        output.append('<div class="date-select">' + select_html + '</div>')

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        if y and m:
            return '%s-%s-%s' % (y, m, 1)
        return data.get(name, None)
