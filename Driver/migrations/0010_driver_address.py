# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0009_auto_20170422_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='address',
            field=models.CharField(default=b'', max_length=300),
        ),
    ]
