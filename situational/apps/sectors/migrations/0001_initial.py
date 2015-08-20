# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import jsonfield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('postcode', models.CharField(max_length=14, db_index=True)),
                ('soc_codes', models.CharField(max_length=200, db_index=True)),
                ('jobs_breakdown', jsonfield.fields.JSONField()),
                ('resident_occupations', jsonfield.fields.JSONField()),
                ('soc_code_data', jsonfield.fields.JSONField()),
                ('is_populating', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
