# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-29 06:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20170623_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogacion',
            name='fin',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='catalogacion',
            name='inicio',
            field=models.FloatField(),
        ),
    ]
