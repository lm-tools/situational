# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('adzuna_id', models.CharField(db_index=True, max_length=255)),
                ('url', models.CharField(max_length=2000, null=True)),
                ('title', models.CharField(max_length=120, null=True)),
                ('salary_max', models.CharField(max_length=120, null=True)),
                ('salary_min', models.CharField(max_length=120, null=True)),
                ('salary_is_predicted', models.CharField(max_length=120, null=True)),
                ('location_name', models.CharField(max_length=120, null=True)),
                ('latitude', models.CharField(max_length=120, null=True)),
                ('longitude', models.CharField(max_length=120, null=True)),
                ('category_name', models.CharField(max_length=120, null=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('company_name', models.CharField(max_length=120, null=True)),
                ('average_company_salary', models.CharField(max_length=120, null=True)),
                ('contract_type', models.CharField(max_length=120, null=True)),
                ('contract_time', models.CharField(max_length=120, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobDiscoveryReport',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('guid', models.UUIDField(primary_key=True, serialize=False, default=uuid.uuid4)),
                ('postcode', models.CharField(max_length=14)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('adzuna_locations', models.CharField(db_index=True, max_length=200)),
                ('jobs', models.ManyToManyField(to='job_discovery.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('response', models.CharField(max_length=50)),
                ('job', models.ForeignKey(to='job_discovery.Job')),
                ('report', models.ForeignKey(to='job_discovery.JobDiscoveryReport')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='jobdiscoveryreport',
            name='location',
            field=models.ForeignKey(to='job_discovery.JobLocation'),
        ),
        migrations.AddField(
            model_name='jobdiscoveryreport',
            name='seen_jobs',
            field=models.ManyToManyField(to='job_discovery.Job', through='job_discovery.Reaction'),
        ),
    ]
