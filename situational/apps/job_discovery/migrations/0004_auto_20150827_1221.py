# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('job_discovery', '0003_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
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
            name='seen_jobs',
            field=models.ManyToManyField(through='job_discovery.Reaction', to='job_discovery.Job'),
        ),
    ]
