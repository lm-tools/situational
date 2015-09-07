# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_discovery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='adzuna_id',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='joblocation',
            name='adzuna_locations',
            field=models.CharField(unique=True, max_length=200),
        ),
    ]
