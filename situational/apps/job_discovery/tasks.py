from celery import shared_task
from celery.utils.log import get_task_logger

from templated_email import send_templated_email

from . import pdf

logger = get_task_logger(__name__)


@shared_task
def send_job_discovery(report, email):
    logger.debug("Sending job discovery report to {}".format(email))

    send_templated_email(
        template_name="job_discovery/emails/job_discovery_report",
        context={"report": report},
        to=[email],
        subject="Your job discovery report",
        attachments=[
            ("job-discovery-report.pdf",
             pdf.render(report),
             "application/pdf"),
        ],
    )
