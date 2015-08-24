from django.template import loader

from . import convertors


class Template():
    def __init__(self, template_name, pdf_converter=convertors.PrinceXML):
        self._convertor = pdf_converter()
        self._django_template = loader.get_template(template_name)

    def render(self, context):
        return self._convertor.convert(
            self._django_template.render(context)
        )
