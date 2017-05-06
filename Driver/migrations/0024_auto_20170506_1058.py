# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Driver', '0023_auto_20170506_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('make', models.CharField(default=b'', max_length=200)),
                ('model', models.CharField(default=b'', max_length=200)),
                ('year', models.IntegerField(default=0)),
                ('id_num', models.IntegerField(default=0)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('temporary', models.BooleanField(default=False)),
                ('selected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(default=b'', max_length=200)),
                ('phone_number', models.CharField(default=b'', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Dispatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(default=b'', max_length=200)),
                ('consecutive_requests', models.IntegerField(default=0)),
                ('last_request_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('current_car_id', models.IntegerField(default=0)),
                ('email', models.CharField(default=b'', max_length=200)),
                ('current_service_key', models.IntegerField(default=1)),
                ('current_request_id', models.IntegerField(default=1)),
                ('phone_number', models.IntegerField(default=0)),
                ('address', models.CharField(default=b'', max_length=300)),
                ('cars', models.ManyToManyField(to='Driver.Car')),
            ],
        ),
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
                ('requester', models.CharField(default=b'', max_length=200)),
                ('confirmed', models.BooleanField(default=False)),
                ('flat_tires', models.CharField(default=b'', max_length=200)),
                ('message', models.CharField(default=b'', max_length=1000)),
                ('in_ditch', models.BooleanField(default=False)),
                ('accident', models.BooleanField(default=False)),
                ('claimed', models.BooleanField(default=False)),
                ('time_claimed', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('car', models.OneToOneField(null=True, default=b'', blank=True, to='Driver.Car')),
                ('contact', models.OneToOneField(null=True, default=b'', blank=True, to='Driver.Contact')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=200)),
                ('cost', models.IntegerField(default=0)),
                ('estimated_time', models.CharField(default=b'', max_length=200)),
                ('provider', models.CharField(default=b'', max_length=200)),
                ('id_num', models.IntegerField(default=1)),
                ('description', models.CharField(default=b'', max_length=500)),
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
