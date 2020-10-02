# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-25 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrobin', '0067_add_display_wip_images_on_public_gallery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commercialgear',
            name='image',
        ),
        migrations.RemoveField(
            model_name='commercialgear',
            name='producer',
        ),
        migrations.RemoveField(
            model_name='retailedgear',
            name='retailer',
        ),
        migrations.RemoveField(
            model_name='gear',
            name='commercial',
        ),
        migrations.RemoveField(
            model_name='gear',
            name='retailed',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='company_description',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='company_website',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='retailer_country',
        ),
        migrations.DeleteModel(
            name='CommercialGear',
        ),
        migrations.DeleteModel(
            name='RetailedGear',
        ),
    ]
