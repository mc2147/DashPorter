# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='service_type',
            new_name='name',
        ),
        migrations.AddField(
            model_name='car',
            name='id_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='car',
            name='name',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='driver',
            name='current_car_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='driver',
            name='current_service_key',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='request',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='service',
            name='id_num',
            field=models.IntegerField(default=0),
        ),
    ]
