# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0012_auto_20170502_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(default=b'', max_length=200)),
                ('phone_number', models.CharField(default=b'', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='request',
            name='car',
            field=models.OneToOneField(default=b'', to='Driver.Car'),
        ),
        migrations.AlterField(
            model_name='request',
            name='time_claimed',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name='request',
            name='contact',
            field=models.OneToOneField(default=b'', to='Driver.Contact'),
        ),
    ]
