import template_to_pdf


def render(history):
    template = template_to_pdf.Template('detailed_history/print.html')
    return template.render({'summary': history})
