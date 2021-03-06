import mimetypes

from django.core.files import File
from django.conf import settings
from django.db import models

from travel_times import constants
from travel_times import mapumental


class TravelTimesMap(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    postcode = models.CharField(
        blank=False, max_length=10, null=False, db_index=True)
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
        client = client()

        image = client.get(
            self.postcode,
            self.width,
            self.height,
            constants.DEPART_AT,
            constants.MAX_TRAVEL_TIME,
        )

        self.mime_type = image.mime_type
        filename = "{}-w{}-h{}.{}".format(
            self.postcode,
            self.width,
            self.height,
            mimetypes.guess_extension(self.mime_type)[0],
        )
        self.image.save(
            filename,
            File(image.file),
            False,
        )
        self.save()

    class Meta:
        unique_together = (
            ('postcode', 'width', 'height'),
        )
