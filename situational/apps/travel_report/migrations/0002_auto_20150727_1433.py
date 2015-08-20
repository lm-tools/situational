# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='travel_times_map',
            field=models.ForeignKey(to='travel_times.TravelTimesMap', null=True),
        ),
    ]
