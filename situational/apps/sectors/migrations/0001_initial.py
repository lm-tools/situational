# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SectorsReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('postcode', models.CharField(max_length=14)),
                ('soc_codes', models.CharField(max_length=200)),
                ('jobs_breakdown', jsonfield.fields.JSONField()),
                ('resident_occupations', jsonfield.fields.JSONField()),
                ('soc_code_data', jsonfield.fields.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
