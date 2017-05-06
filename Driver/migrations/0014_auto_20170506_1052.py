# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0013_auto_20170506_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='car',
            field=models.OneToOneField(null=True, default=b'', to='Driver.Car'),
        ),
        migrations.AlterField(
            model_name='request',
            name='contact',
            field=models.OneToOneField(null=True, default=b'', to='Driver.Contact'),
        ),
    ]
