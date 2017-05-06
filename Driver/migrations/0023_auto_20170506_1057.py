# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0022_auto_20170506_1057'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Car',
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
        migrations.RemoveField(
            model_name='dispatch',
            name='requests',
        ),
        migrations.RemoveField(
            model_name='dispatch',
            name='user',
        ),
        migrations.DeleteModel(
            name='PaymentInfo',
        ),
        migrations.DeleteModel(
            name='Repair_Shop',
        ),
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='Dispatch',
        ),
        migrations.DeleteModel(
            name='Request',
        ),
    ]
