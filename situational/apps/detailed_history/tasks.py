from celery import shared_task
from celery.utils.log import get_task_logger

from templated_email import send_templated_email
import template_to_pdf

logger = get_task_logger(__name__)


@shared_task
def send_detailed_history(history, email):
    logger.debug("Sending detailed history report to {}".format(email))

    pdf_template = template_to_pdf.Template('detailed_history/print.html')
    pdf = pdf_template.render({'summary': history})

    send_templated_email(
        template_name="detailed_history/emails/detailed_history_report",
        context={"summary": history},
        to=[email],
        subject="Your detailed history report",
        attachments=[
            ("history-report.pdf",
             pdf,
             "application/pdf"),
        ],
    )
