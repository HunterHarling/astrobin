# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-11-17 17:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('astrobin', '0078_add_recovery_ignored'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerevision',
            name='recovery_ignored',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
