from celery import shared_task
from celery.utils.log import get_task_logger

from templated_email import send_templated_email

from . import pdf

logger = get_task_logger(__name__)


@shared_task
def send_quick_history(history, email):
    logger.debug("Sending quick history report to {}".format(email))

    send_templated_email(
        template_name="quick_history/emails/quick_history_report",
        context={"report": history},
        to=[email],
        subject="Your detailed history report",
        attachments=[
            ("quick-history-report.pdf",
             pdf.render(history),
             "application/pdf"),
        ],
    )
