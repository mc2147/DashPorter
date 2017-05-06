# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Driver', '0011_auto_20170502_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(default=b'', max_length=200)),
                ('consecutive_requests', models.IntegerField(default=0)),
                ('last_request_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='request',
            name='time_claimed',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 2, 21, 44, 11, 207678)),
        ),
        migrations.AddField(
            model_name='dispatch',
            name='requests',
            field=models.ManyToManyField(to='Driver.Request'),
        ),
        migrations.AddField(
            model_name='dispatch',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
