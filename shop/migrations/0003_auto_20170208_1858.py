# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 18:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20170108_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='latest',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='games',
            name='released',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchased',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]