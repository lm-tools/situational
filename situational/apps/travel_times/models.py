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
        null=True,
        upload_to='travel_times_maps',
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
    def get(self, postcode, width, height):
        travel_times_map, _created = TravelTimesMap.objects.get_or_create(
            postcode=postcode,
            width=width,
            height=height,
            )

        if not travel_times_map.image:
            populator = TravelTimesMapPopulator()
            travel_times_map = populator.populate(travel_times_map)

        return travel_times_map


class TravelTimesMapPopulator(object):
    def __init__(self, client=None):
        if not client:
            client = getattr(settings, 'MAPUMENTAL_CLIENT', mapumental.Client)
        self.client = client()
        self.depart_at = '0800'
        self.arrive_before = '0930'

    def populate(self, map):
        image = self.client.get(
            map.postcode,
            map.width,
            map.height,
            self.depart_at,
            self.arrive_before,
            )

        map.mime_type = image.mime_type
        map.image.save(
            "%s-w%s-h%s" % (map.postcode, map.width, map.height),
            File(image.file),
            False,
            )
        map.save()

        return map
