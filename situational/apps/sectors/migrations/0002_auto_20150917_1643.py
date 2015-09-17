# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sectors', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sectorsreport',
            name='jobs_breakdown',
        ),
        migrations.RemoveField(
            model_name='sectorsreport',
            name='postcode',
        ),
        migrations.RemoveField(
            model_name='sectorsreport',
            name='resident_occupations',
        ),
    ]
