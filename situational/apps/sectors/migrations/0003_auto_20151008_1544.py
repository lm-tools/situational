# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sectors', '0002_auto_20150917_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectorsreport',
            name='soc_codes',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
