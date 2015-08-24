from celery import shared_task
from celery.utils.log import get_task_logger

from templated_email import send_templated_email

from . import pdf

logger = get_task_logger(__name__)


@shared_task
def send_detailed_history(history, email):
    logger.debug("Sending detailed history report to {}".format(email))

    send_templated_email(
        template_name="detailed_history/emails/detailed_history_report",
        context={"summary": history},
        to=[email],
        subject="Your detailed history report",
        attachments=[
            ("history-report.pdf",
             pdf.render(history),
             "application/pdf"),
        ],
    )
