# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0003_report_is_populating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='place_name',
        ),
    ]
