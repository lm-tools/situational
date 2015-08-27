# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_discovery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='average_company_salary',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='category_name',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='company_name',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='contract_time',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='contract_type',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='latitude',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='location_name',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='longitude',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='salary_is_predicted',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='salary_max',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='salary_min',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='title',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
