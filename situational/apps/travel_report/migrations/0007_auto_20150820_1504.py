# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0006_auto_20150819_1717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelreport',
            name='latest_jobs',
        ),
        migrations.RemoveField(
            model_name='travelreport',
            name='top_categories',
        ),
        migrations.RemoveField(
            model_name='travelreport',
            name='top_companies',
        ),
    ]
