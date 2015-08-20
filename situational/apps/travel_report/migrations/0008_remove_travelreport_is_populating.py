# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0007_auto_20150820_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelreport',
            name='is_populating',
        ),
    ]
