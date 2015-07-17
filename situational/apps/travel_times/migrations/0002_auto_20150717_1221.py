# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_times', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traveltimesmap',
            name='image',
            field=models.ImageField(null=True, height_field='actual_height', upload_to='travel_times_maps', width_field='actual_width'),
        ),
    ]
