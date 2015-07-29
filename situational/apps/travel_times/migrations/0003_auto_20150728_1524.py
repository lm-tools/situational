# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_times', '0002_auto_20150717_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traveltimesmap',
            name='postcode',
            field=models.CharField(max_length=10, db_index=True),
        ),
    ]
