# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sectors', '0002_remove_report_is_populating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Report',
            new_name='SectorsReport',
        ),
    ]
