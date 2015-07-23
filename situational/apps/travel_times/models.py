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

    @property
    def has_image(self):
        return bool(self.image)

    def download_image(self):
        client = getattr(settings, 'MAPUMENTAL_CLIENT', mapumental.Client)
        self.client = client()
        depart_at = getattr(settings, 'MAPUMENTAL_DEPART_AT', '0800')
        arrive_before = getattr(
            settings, 'MAPUMENTAL_ARRIVE_BEFORE', '0930')

        image = client.get(
            self.postcode,
            self.width,
            self.height,
            depart_at,
            arrive_before,
        )

        self.mime_type = image.mime_type
        self.image.save(
            "%s-w%s-h%s" % (self.postcode, self.width, self.height),
            File(image.file),
            False,
            )
        self.save()

    class Meta:
        unique_together = (
            ('postcode', 'width', 'height'),
        )
