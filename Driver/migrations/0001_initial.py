# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('make', models.CharField(default=b'', max_length=200)),
                ('model', models.CharField(default=b'', max_length=200)),
                ('year', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('email', models.CharField(default=b'', max_length=200)),
                ('current_request_id', models.IntegerField(default=0)),
                ('cars', models.ManyToManyField(to='Driver.Car')),
            ],
        ),
        migrations.CreateModel(
            name='new_model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('test', models.CharField(default=b'', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Repair_Shop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(default=b'', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('id_num', models.IntegerField(default=0)),
                ('service', models.CharField(default=b'', max_length=200)),
                ('cost', models.IntegerField(default=0)),
                ('initial_ETA', models.CharField(default=b'', max_length=200)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('provider', models.CharField(default=b'', max_length=200)),
                ('requester', models.OneToOneField(to='Driver.Driver')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('service_type', models.CharField(default=b'', max_length=200)),
                ('cost', models.IntegerField(default=0)),
                ('estimated_time', models.CharField(default=b'', max_length=200)),
                ('provider', models.CharField(default=b'', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='requests',
            field=models.ManyToManyField(to='Driver.Request'),
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
