# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import jsonfield.fields
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('travel_times', '0002_auto_20150717_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('postcode', models.CharField(max_length=14)),
                ('place_name', models.CharField(max_length=255, blank=True)),
                ('location_json', jsonfield.fields.JSONField()),
                ('top_categories', jsonfield.fields.JSONField()),
                ('top_companies', jsonfield.fields.JSONField()),
                ('latest_jobs', jsonfield.fields.JSONField()),
                ('travel_times_map', models.ForeignKey(to='travel_times.TravelTimesMap')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
