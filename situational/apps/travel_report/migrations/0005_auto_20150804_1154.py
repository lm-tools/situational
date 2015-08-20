# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_report', '0004_remove_report_place_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='postcode',
            field=models.CharField(max_length=14, db_index=True),
        ),
    ]
