from django.conf import settings

from celery import chord, shared_task
from celery.utils.log import get_task_logger
from redlock import Redlock

from sectors import helpers
from templated_email import send_templated_email

logger = get_task_logger(__name__)
population_timeout = settings.REPORT_POPULATION_TIMEOUT
dlm = Redlock([settings.REDIS_URL])  # Distibuted Lock Manager


@shared_task
def populate_report(report):
    lock = dlm.lock("sectors-report-{}".format(report.pk), population_timeout)
    sector_string = "Sector report for codes {}"
    sector_report = sector_string.format(report.soc_codes,)
    if not lock:
        logger.debug("{} is already populating".format(sector_report))
        return

    logger.debug("Populating {}".format(sector_report))

    logger.debug("Running all the sub tasks")
    sub_tasks = (
        soc_code_data.si(report),
    )
    callback = release_lock.si(report.pk, lock)
    for task in sub_tasks + (callback,):
        task.set(expires=population_timeout)
    chord(sub_tasks, callback).delay()


@shared_task
def release_lock(identifier, lock):
    logger.debug("Releasing lock for report '{}'".format(identifier))
    dlm.unlock(lock)


@shared_task
def soc_code_data(report):
    soc_codes_list = report.soc_codes.split(",")
    logger.debug("Getting soc_code_data for {}".format(soc_codes_list))
    lmi_client = helpers.LMIForAllClient()
    soc_code_data = {}
    for soc_code in soc_codes_list:
        soc_code_int = int(soc_code)
        soc_code_data[soc_code_int] = {
            'pay': lmi_client.pay(soc_code_int),
            'hours_worked': lmi_client.hours_worked(soc_code_int),
            'info': lmi_client.soc_code_info(soc_code_int)
        }
    report.soc_code_data = soc_code_data
    report.save(update_fields=['soc_code_data'])


@shared_task
def send_report(report, email):
    subject = "What sort of jobs you could do"
    logger.debug("Sending report {} to {}".format(report.id, email))
    send_templated_email(
        template_name="sectors/emails/sectors_report",
        context={"report": report},
        to=[email],
        subject=subject,
        attachments=[
            ("sectors-report.pdf",
             report.to_pdf(),
             "application/pdf"),
        ],
    )
