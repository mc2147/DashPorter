# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0006_auto_20170420_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='car',
            name='temporary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='information',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
