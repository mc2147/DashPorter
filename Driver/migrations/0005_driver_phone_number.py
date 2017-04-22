# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0004_auto_20170420_0201'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='phone_number',
            field=models.IntegerField(default=0),
        ),
    ]
