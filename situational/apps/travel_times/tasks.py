from celery import shared_task

@shared_task
def download_map_image(travel_times_map):
    travel_times_map.download_image()
