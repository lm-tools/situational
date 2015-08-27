# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import uuid
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobDiscoveryReport',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('guid', models.UUIDField(serialize=False, primary_key=True, default=uuid.uuid4, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobLocation',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('postcode', models.CharField(max_length=14)),
                ('location', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
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
            field=models.ManyToManyField(through='job_discovery.Reaction', to='job_discovery.Job'),
        ),
        migrations.AddField(
            model_name='job',
            name='location',
            field=models.ForeignKey(to='job_discovery.JobLocation'),
        ),
    ]
