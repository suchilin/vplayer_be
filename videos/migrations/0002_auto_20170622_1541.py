# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 20:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='creado',
        ),
        migrations.AddField(
            model_name='video',
            name='path',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
