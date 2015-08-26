import uuid

from model_utils.models import TimeStampedModel

from django.db import models
from .adzuna import Adzuna


class Job(TimeStampedModel):
    adzuna_id = models.CharField(max_length=255, db_index=True)
    url = models.CharField(max_length=2000, null=True)
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


class JobLocation(models.Model):
    adzuna_locations = models.CharField(max_length=200, db_index=True)
    jobs = models.ManyToManyField(Job)

    def import_jobs(self):
        az = Adzuna()
        locations = self.adzuna_locations.split(",")
        az_jobs = az.jobs_at_location(
            locations[0],
            locations[1],
            locations[2],
            50
        )
        for az_job in az_jobs:
            company = az_job.get('company', {})
            adzuna_id = az_job.get('id')
            job, _ = Job.objects.update_or_create(
                adzuna_id=adzuna_id,
                defaults={
                    "url": az_job.get('redirect_url'),
                    "title": az_job.get('title'),
                    "salary_max": az_job.get('salary_max'),
                    "salary_min": az_job.get('salary_min'),
                    "salary_is_predicted": az_job.get('salary_is_predicted'),
                    "location_name": az_job.get('location', {})
                                           .get('display_name'),
                    "latitude": az_job.get('latitude'),
                    "longitude": az_job.get('longitude'),
                    "category_name": az_job.get('category', {}).get('label'),
                    "description": az_job.get('description'),
                    "company_name": company.get('display_name'),
                    "average_company_salary": company.get('average_salary'),
                    "contract_type": az_job.get('contract_type'),
                    "contract_time": az_job.get('contract_time'),
                }
            )
            self.jobs.add(job)


class JobDiscoveryReport(TimeStampedModel):
    guid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    postcode = models.CharField(blank=False, null=False, max_length=14)
    location = models.ForeignKey(JobLocation)
    seen_jobs = models.ManyToManyField(Job, through='Reaction')

    @property
    def reactions(self):
        return Reaction.objects.filter(report=self)

    def add_reaction(self, job, response):
        Reaction.objects.create(report=self, job=job, response=response)

    def get_suggestion(self):
        job_ids = self.seen_jobs.values_list('id', flat=True)
        unseen_jobs = self.location.jobs.exclude(id__in=job_ids)
        job = unseen_jobs.order_by('?').first()
        if job:
            return job
        else:
            self.location.import_jobs()
            return unseen_jobs.order_by('?').first()


class Reaction(TimeStampedModel):
    job = models.ForeignKey(Job)
    report = models.ForeignKey(JobDiscoveryReport)
    response = models.CharField(max_length=50)
