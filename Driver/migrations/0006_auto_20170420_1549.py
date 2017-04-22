# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0005_driver_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='requester',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
