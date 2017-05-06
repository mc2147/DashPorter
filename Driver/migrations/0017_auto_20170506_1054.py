# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0016_auto_20170506_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dispatch',
            name='requests',
        ),
        migrations.AlterField(
            model_name='request',
            name='contact',
            field=models.OneToOneField(primary_key=True, default=b'', to='Driver.Contact'),
        ),
    ]
