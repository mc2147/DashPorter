# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0025_request_car_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='phone_num',
            field=models.IntegerField(default=0),
        ),
    ]
