# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0002_auto_20170419_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='current_request_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='driver',
            name='current_service_key',
            field=models.IntegerField(default=1),
        ),
    ]
