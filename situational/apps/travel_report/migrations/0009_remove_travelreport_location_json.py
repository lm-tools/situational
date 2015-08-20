# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0008_remove_travelreport_is_populating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelreport',
            name='location_json',
        ),
    ]
