# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-12 20:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrobin_apps_platesolving', '0009_platesolvingadvancedsettings_scaled_font_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='advanced_annotations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='solution',
            name='advanced_annotations_regular',
            field=models.TextField(blank=True, null=True),
        ),
    ]