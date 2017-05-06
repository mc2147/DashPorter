# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0015_auto_20170506_1053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='id',
        ),
        migrations.AlterField(
            model_name='request',
            name='car',
            field=models.OneToOneField(primary_key=True, default=b'', serialize=False, to='Driver.Car'),
        ),
        migrations.AlterField(
            model_name='request',
            name='contact',
            field=models.OneToOneField(primary_key=True, default=b'', to='Driver.Contact'),
        ),
    ]
