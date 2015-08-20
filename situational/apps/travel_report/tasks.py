from django.conf import settings
from django.db import transaction

from celery import chord, shared_task
from celery.utils.log import get_task_logger
from redlock import Redlock

from templated_email import send_templated_email
from travel_times.models import TravelTimesMap
from travel_times import constants

from . import helpers

logger = get_task_logger(__name__)
population_timeout = settings.REPORT_POPULATION_TIMEOUT
dlm = Redlock([settings.REDIS_URL])  # Distibuted Lock Manager


@shared_task
def populate_report(report):
    lock = dlm.lock("populate-travel-report-{}".format(report.pk),
                    population_timeout)
    if not lock:
        logger.debug(
            "Travel report '%s' is already populating".format(report.postcode)
        )
        return

    logger.debug("Populating travel report '{}'".format(report.postcode))

    if not report.location_json:
        logger.debug("No Location JSON yet, getting it form MaPit")
        report.location_json = helpers.geocode(report.postcode)
        report.save(update_fields=['location_json'])

    logger.debug("Running all the sub tasks")
    sub_tasks = (
        travel_times_map.si(report),
    )
    callback = release_lock.si(report.pk, lock)
    for task in sub_tasks + (callback,):
        task.set(expires=population_timeout)
    chord(sub_tasks, callback).delay()


@shared_task
def release_lock(identifier, lock):
    logger.debug("Releasing lock for travel report '{}'".format(identifier))
    dlm.unlock(lock)


@shared_task
def travel_times_map(report):
    logger.debug("Getting travel times map")
    travel_times_map, _created = TravelTimesMap.objects.get_or_create(
        postcode=report.postcode,
        width=constants.MAP_WIDTH,
        height=constants.MAP_HEIGHT,
    )
    if not travel_times_map.has_image:
        travel_times_map.download_image()
    report.travel_times_map = travel_times_map
    report.save(update_fields=['travel_times_map'])


@shared_task
def top_categories(report):
    logger.debug("Getting top categories")
    report.top_categories = \
        helpers.top_categories_for_postcode(report.postcode)
    report.save(update_fields=['top_categories'])


@shared_task
def top_companies(report):
    logger.debug("Getting top companies")
    report.top_companies = \
        helpers.top_companies_for_postcode(report.postcode)
    report.save(update_fields=['top_companies'])


@shared_task
def latest_jobs(report):
    logger.debug("Getting latest jobs")
    report.latest_jobs = \
        helpers.latest_jobs_for_postcode(report.postcode)
    report.save(update_fields=['latest_jobs'])


@shared_task
def send_report(report, email):
    subject = "Your travel time map report for {}".format(report.postcode)
    logger.debug("Sending report {} to {}".format(report.id, email))
    send_templated_email(
        template_name="travel_report/emails/travel_report",
        context={"report": report},
        to=[email],
        subject=subject,
        attachments=[
            ("travel-report-{}.pdf".format(report.postcode),
             report.to_pdf(),
             "application/pdf"),
        ],
    )
