# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0003_auto_20170419_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.CharField(default=b'', max_length=500),
        ),
        migrations.AlterField(
            model_name='service',
            name='id_num',
            field=models.IntegerField(default=1),
        ),
    ]
