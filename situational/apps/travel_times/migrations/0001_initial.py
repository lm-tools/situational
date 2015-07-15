# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TravelTimesMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('postcode', models.CharField(max_length=10)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('image', models.ImageField(null=True, width_field='actual_width', upload_to='', height_field='actual_height')),
                ('actual_width', models.IntegerField(null=True)),
                ('actual_height', models.IntegerField(null=True)),
                ('mime_type', models.CharField(null=True, max_length=255)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='traveltimesmap',
            unique_together=set([('postcode', 'width', 'height')]),
        ),
    ]
