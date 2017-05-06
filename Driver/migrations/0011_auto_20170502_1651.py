# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0010_driver_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cardholder_name', models.CharField(default=b'', max_length=200)),
                ('billing_address', models.CharField(default=b'', max_length=200)),
                ('city_state_zip', models.CharField(default=b'', max_length=200)),
                ('card_number', models.IntegerField(default=0)),
                ('expiry_date', models.IntegerField(default=0)),
                ('security_code', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='claimed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='request',
            name='time_claimed',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 2, 16, 51, 9, 50044)),
        ),
    ]
