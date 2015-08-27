# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobDiscoveryReport',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('guid', models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4, serialize=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobLocation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('postcode', models.CharField(max_length=14)),
                ('adzuna_locations', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
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
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.ForeignKey(to='job_discovery.JobLocation'),
        ),
    ]
