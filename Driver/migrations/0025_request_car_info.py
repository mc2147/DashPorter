# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0024_auto_20170506_1058'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='car_info',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
