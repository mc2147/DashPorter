# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0019_auto_20170506_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='car',
        ),
        migrations.RemoveField(
            model_name='request',
            name='contact',
        ),
        migrations.AddField(
            model_name='driver',
            name='cars',
            field=models.ManyToManyField(to='Driver.Car'),
        ),
        migrations.AddField(
            model_name='driver',
            name='requests',
            field=models.ManyToManyField(to='Driver.Request'),
        ),
        migrations.AddField(
            model_name='request',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
