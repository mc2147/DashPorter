# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0008_auto_20170422_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='information',
            new_name='flat_tires',
        ),
    ]
