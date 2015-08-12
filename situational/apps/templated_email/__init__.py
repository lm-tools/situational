from django.core.mail import EmailMultiAlternatives
from django.template import loader


def send_templated_email(template_name=None, context=None, **kwargs):
    plain_text_template = loader.get_template("{}.txt".format(template_name))
    html_template = loader.get_template("{}.html".format(template_name))

    message = EmailMultiAlternatives(
        body=plain_text_template.render(context),
        **kwargs
    )
    message.attach_alternative(
        html_template.render(context),
        "text/html",
    )
    message.send()
