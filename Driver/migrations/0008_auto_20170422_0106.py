# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0007_auto_20170421_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='accident',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='in_ditch',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='message',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]
