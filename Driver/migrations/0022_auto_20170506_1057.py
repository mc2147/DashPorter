# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0021_auto_20170506_1056'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='user',
        ),
        migrations.DeleteModel(
            name='Driver',
        ),
    ]
