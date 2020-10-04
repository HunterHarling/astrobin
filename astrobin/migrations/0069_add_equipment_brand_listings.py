# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-26 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrobin', '0068_remove_commercial_and_related_gear_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='gear',
            name='equipment_brand_listings',
            field=models.ManyToManyField(editable=False, related_name='gear_items', to='astrobin_apps_equipment.EquipmentBrandListing'),
        ),
    ]