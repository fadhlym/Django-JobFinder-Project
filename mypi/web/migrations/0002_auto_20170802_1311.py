# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 06:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kerja',
            name='comp_desc',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='kerja',
            name='jobs_desc',
            field=models.CharField(default='', max_length=255),
        ),
    ]
