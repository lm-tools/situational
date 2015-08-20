# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0002_auto_20150727_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='is_populating',
            field=models.BooleanField(default=False),
        ),
    ]
