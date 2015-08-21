# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sectors', '0003_auto_20150820_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectorsreport',
            name='postcode',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='sectorsreport',
            name='soc_codes',
            field=models.CharField(max_length=200),
        ),
    ]
