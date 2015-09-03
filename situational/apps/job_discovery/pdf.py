import template_to_pdf


def render(report):
    template = template_to_pdf.Template('job_discovery/print.html')
    return template.render({'report': report})
