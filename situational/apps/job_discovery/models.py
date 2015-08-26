from django.db import models
import uuid
from model_utils.models import TimeStampedModel


class JobDiscoveryReport(TimeStampedModel):
    postcode = models.CharField(
        blank=False, null=False, max_length=14, db_index=True)
    guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
