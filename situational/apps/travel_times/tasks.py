from celery import shared_task

from .models import TravelTimesMapPopulator

@shared_task
def download_map_image(travel_times_map):
    TravelTimesMapPopulator().populate(travel_times_map)
