import template_to_pdf


def render(history):
    template = template_to_pdf.Template('quick_history/print.html')
    return template.render({'report': history})
