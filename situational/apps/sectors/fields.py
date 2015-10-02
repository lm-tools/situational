import json

from django import forms


class MultiCharFieldWidget(forms.widgets.MultiWidget):
    def __init__(self, count, attrs=None):
        self.count = count
        widgets = [
            forms.TextInput(attrs={"class": "form-control"})
            for i in range(self.count)
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return json.loads(value)
        else:
            return ['' for i in range(self.count)]

    def format_output(self, rendered_widgets):
        return "<ul class='multi-char-field-widget'>" + "".join(
            ["<li>%s</li>" % w for w in rendered_widgets]
        ) + "</ul>"


class MultiCharField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):

        # Or define a different message for each field.
        kwargs['fields'] = []
        for i, f in enumerate(range(kwargs['count'])):
            kwargs['fields'].append(
                forms.CharField(required=False),
            )

        self.widget = MultiCharFieldWidget(kwargs['count'])
        del kwargs['count']
        super().__init__(*args, **kwargs)

    def compress(self, values):
        return values
