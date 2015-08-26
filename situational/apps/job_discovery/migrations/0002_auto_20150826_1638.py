# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('job_discovery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobdiscoveryreport',
            name='id',
        ),
        migrations.AddField(
            model_name='jobdiscoveryreport',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, serialize=False, primary_key=True),
        ),
    ]
