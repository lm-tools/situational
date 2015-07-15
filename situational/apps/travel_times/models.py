import uuid

from django.core.files import File
from django.conf import settings
from django.db import models

from travel_times import mapumental


class TravelTimesMap(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    postcode = models.CharField(blank=False, max_length=10, null=False)
    width = models.IntegerField(blank=False, null=False)
    height = models.IntegerField(blank=False, null=False)
    image = models.ImageField(
        width_field='actual_width',
        height_field='actual_height',
        null=True
        )
    actual_width = models.IntegerField(null=True)
    actual_height = models.IntegerField(null=True)
    mime_type = models.CharField(max_length=255, null=True)

    def read_image(self):
        self.image.open()
        return self.image.read()

    class Meta:
        unique_together = (
            ('postcode', 'width', 'height'),
            )


class TravelTimesMapRepository(object):
    def __init__(self, client=None):
        if not client:
            client = getattr(settings, 'MAPUMENTAL_CLIENT', mapumental.Client)
        self.client = client()
        self.depart_at = '0800'
        self.arrive_before = '0930'

    def get(self, postcode, width, height):
        travel_times_map, _created = TravelTimesMap.objects.get_or_create(
            postcode=postcode,
            width=width,
            height=height,
            )

        if not travel_times_map.image:
            print(
                "Fetching travel time map for %s, w=%s, h=%s" %
                (postcode, width, height)
                )
            image = self.client.get(
                postcode,
                width,
                height,
                self.depart_at,
                self.arrive_before,
                )
            travel_times_map.mime_type = image.mime_type
            travel_times_map.image.save(
                str(uuid.uuid4()),
                File(image.file),
                False,
                )
            travel_times_map.save()

        return travel_times_map
