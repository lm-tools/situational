# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('job_discovery', '0002_auto_20150907_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='adzuna_locations',
            field=django.contrib.postgres.fields.ArrayField(default=list, base_field=models.CharField(max_length=200), size=None),
        ),
    ]
