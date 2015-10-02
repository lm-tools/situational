import template_to_pdf


def render(report):
    template = template_to_pdf.Template('job_discovery/print.html')
    context = {
        "jobs": report.liked_jobs,
        "job_pool_location": report.location.adzuna_locations,
    }
    return template.render(context)
