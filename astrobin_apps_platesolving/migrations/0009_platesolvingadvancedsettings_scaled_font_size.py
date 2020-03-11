# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-10 19:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('astrobin_apps_platesolving', '0008_rename_pixinsight_annotation_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='platesolvingadvancedsettings',
            name='scaled_font_size',
            field=models.CharField(choices=[(b'S', 'Small'), (b'M', 'Medium'), (b'L', 'Large')], default=b'M',
                                   max_length=1, verbose_name='Scaled font size',
                                   help_text='Font size of the annotations on your main image page'),
        ),
    ]
