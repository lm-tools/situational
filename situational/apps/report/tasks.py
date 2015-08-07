from django.conf import settings
from django.core.mail import EmailMessage
from django.db import transaction

from celery import chord, shared_task
from celery.utils.log import get_task_logger
from redlock import Redlock

from travel_times.models import TravelTimesMap
from travel_times import constants

from report import helpers

logger = get_task_logger(__name__)
population_timeout = settings.REPORT_POPULATION_TIMEOUT
dlm = Redlock([settings.REDIS_URL])  # Distibuted Lock Manager


@shared_task
def populate_report(report):
    lock = dlm.lock("populate-report-{}".format(report.pk), population_timeout)
    if not lock:
        logger.debug("Report '%s' is already populating" % report.postcode)
        return

    logger.debug("Populating report '{}'".format(report.postcode))

    if not report.location_json:
        logger.debug("No Location JSON yet, getting it form MaPit")
        report.location_json = helpers.geocode(report.postcode)
        report.save(update_fields=['location_json'])

    logger.debug("Running all the sub tasks")
    sub_tasks = (
        travel_times_map.si(report),
        top_categories.si(report),
        top_companies.si(report),
        latest_jobs.si(report),
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
    logger.debug("Sending report {} to {}".format(report.id, email))
    EmailMessage(
        subject="Labour report for {}".format(report.postcode),
        body="Attached please find your report.",
        to=[email],
        attachments=[
            ("{}-report.pdf".format(report.postcode),
             report.to_pdf(),
             "application/pdf"),
        ],
    ).send()
