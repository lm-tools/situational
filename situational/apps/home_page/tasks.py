from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger
from redlock import Redlock

from templated_email import send_templated_email


logger = get_task_logger(__name__)
population_timeout = settings.REPORT_POPULATION_TIMEOUT
dlm = Redlock([settings.REDIS_URL])  # Distibuted Lock Manager


@shared_task
def send_feedback(name, email, content, tool, feedback_type):
    subject = "Feedback: {} - {}".format(tool, feedback_type)
    send_templated_email(
        template_name="home_page/emails/feedback",
        context={
            "content": content,
            "from": {
                "name": name,
                "email": email
            }
        },
        to=["feedback@lm-tools.com"],
        subject=subject
    )
