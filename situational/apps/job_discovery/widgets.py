from itertools import chain

from django import forms
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class MultipleSubmitButton(forms.Widget):
    def __init__(self, attrs={}, choices=()):
        super().__init__(attrs)
        self.choices = list(choices)

    def value_from_datadict(self, data, files, name):
        # IE posts the inner html of the clicked button instead of the value
        value = data.get(name, None)
        if value in dict(self.choices):
            return value
        else:
            inside_out_choices = dict([(v, k) for (k, v) in self.choices])
            if value in inside_out_choices:
                return inside_out_choices[value]
        return None

    def render(self, name, value, attrs=None, choices=()):
        # currently this widget ignores value
        attrs = self.build_attrs(attrs)
        choices = chain(self.choices, choices)

        return mark_safe(
            '<ul%s>\n%s\n</ul>\n' % (flatatt(attrs),
                                     self._render_list_items(name, choices))
        )

    def _render_list_items(self, name, choices):
        return '\n'.join(
            ('<li>%s</li>' % self._render_button(name, value, label)
             for value, label in choices)
        )

    def _render_button(self, name, value, label):
        attrs = {
            "type": "submit",
            "name": name,
            "value": value,
        }
        return format_html('<button{}>{}</button>', flatatt(attrs), label)
