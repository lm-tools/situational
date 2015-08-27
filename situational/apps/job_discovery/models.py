import uuid

from model_utils.models import TimeStampedModel

from django.db import models


class JobLocation(models.Model):
    postcode = models.CharField(
        blank=False, null=False, max_length=14
    )
    adzuna_locations = models.CharField(
        blank=False, null=False, max_length=200
    )

    def import_jobs(self):
        pass


class Job(TimeStampedModel):
    location = models.ForeignKey(JobLocation)


class JobDiscoveryReport(TimeStampedModel):
    location = models.ForeignKey(JobLocation)
    guid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    seen_jobs = models.ManyToManyField(Job, through='Reaction')

    @property
    def reactions(self):
        return Reaction.objects.filter(report=self)

    def add_reaction(self, job, response):
        Reaction.objects.create(report=self, job=job, response=response)

    def get_suggestion(self):
        job_ids = self.seen_jobs.values_list('id', flat=True)
        unseen_jobs = Job.objects.exclude(id__in=job_ids)
        job = unseen_jobs.filter(location=self.location).order_by('?').first()
        return job
        # if job None CamilleTODO: import some jobs!


class Reaction(TimeStampedModel):
    job = models.ForeignKey(Job)
    report = models.ForeignKey(JobDiscoveryReport)
    response = models.CharField(max_length=50)
