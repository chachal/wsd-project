# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-18 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20170217_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='url',
            field=models.URLField(default=None),
        ),
    ]
