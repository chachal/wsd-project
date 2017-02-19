# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-18 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_verifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verifications',
            name='user',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='confcode',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.DeleteModel(
            name='Verifications',
        ),
    ]
