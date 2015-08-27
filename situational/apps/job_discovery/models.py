import uuid

from model_utils.models import TimeStampedModel

from django.db import models
from .adzuna import Adzuna


class JobLocation(models.Model):
    postcode = models.CharField(
        blank=False, null=False, max_length=14
    )
    adzuna_locations = models.CharField(
        blank=False, null=False, max_length=200
    )

    def import_jobs(self):
        az = Adzuna()
        locations = self.adzuna_locations.split(",")
        jobs = az.jobs_at_location(
            locations[0],
            locations[1],
            locations[2],
            50
        )
        for job in jobs:
            company = job.get('company', {})
            Job.objects.create(
                location=self,
                title=job.get('title'),
                salary_max=job.get('salary_max'),
                salary_min=job.get('salary_min'),
                salary_is_predicted=job.get('salary_is_predicted'),
                location_name=job.get('location', {}).get('display_name'),
                latitude=job.get('latitude'),
                longitude=job.get('longitude'),
                category_name=job.get('category', {}).get('label'),
                description=job.get('description'),
                company_name=company.get('display_name'),
                average_company_salary=company.get('average_salary'),
                contract_type=job.get('contract_type'),
                contract_time=job.get('contract_time'),
            )


class Job(TimeStampedModel):
    location = models.ForeignKey(JobLocation)
    title = models.CharField(max_length=120, null=True)
    salary_max = models.CharField(max_length=120, null=True)
    salary_min = models.CharField(max_length=120, null=True)
    salary_is_predicted = models.CharField(max_length=120, null=True)
    location_name = models.CharField(max_length=120, null=True)
    latitude = models.CharField(max_length=120, null=True)
    longitude = models.CharField(max_length=120, null=True)
    category_name = models.CharField(max_length=120, null=True)
    description = models.CharField(max_length=1000, null=True)
    company_name = models.CharField(max_length=120, null=True)
    average_company_salary = models.CharField(max_length=120, null=True)
    contract_type = models.CharField(max_length=120, null=True)
    contract_time = models.CharField(max_length=120, null=True)


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
        unseen_location_jobs = unseen_jobs.filter(location=self.location)
        if unseen_location_jobs.count() == 0:
            self.location.import_jobs()
        job = unseen_location_jobs.order_by('?').first()
        return job


class Reaction(TimeStampedModel):
    job = models.ForeignKey(Job)
    report = models.ForeignKey(JobDiscoveryReport)
    response = models.CharField(max_length=50)
