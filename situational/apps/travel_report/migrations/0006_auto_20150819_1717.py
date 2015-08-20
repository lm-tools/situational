# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0005_auto_20150804_1154'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Report',
            new_name='TravelReport',
        ),
    ]
