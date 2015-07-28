from django.db import transaction

from celery import shared_task
from celery.utils.log import get_task_logger

from travel_times.models import TravelTimesMap
from travel_times.views import MapView

from report import helpers

logger = get_task_logger(__name__)


@shared_task
def populate_report(report):
    logger.debug("Populating a new report")

    if not report.location_json:
        logger.debug("No Location JSON yet, getting it form MaPit")
        report.location_json = helpers.geocode(report.postcode)
        report.save(update_fields=['location_json'])

    logger.debug("Running all the sub tasks")
    travel_times_map.delay(report)
    place_name.delay(report)
    top_categories.delay(report)
    top_companies.delay(report)
    latest_jobs.delay(report)


@shared_task
def travel_times_map(report):
    logger.debug("Getting travel times map")
    travel_times_map, _created = TravelTimesMap.objects.get_or_create(
        postcode=report.postcode,
        width=MapView.default_width,
        height=MapView.default_height,
    )
    if not travel_times_map.has_image:
        travel_times_map.download_image()
    report.travel_times_map = travel_times_map
    report.save(update_fields=['travel_times_map'])


@shared_task
def place_name(report):
    logger.debug("Getting place name")
    report.place_name = helpers.place_name_from_location(
        report.location_json['wgs84_lat'],
        report.location_json['wgs84_lon'],
    )['Name']
    logger.debug("place_name set to {0}".format(report.place_name))
    report.save(update_fields=['place_name'])


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
