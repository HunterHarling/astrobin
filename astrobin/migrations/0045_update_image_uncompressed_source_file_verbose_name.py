# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-16 21:35
from __future__ import unicode_literals

from django.db import migrations, models

import astrobin.models
import common.validators.file_validator


class Migration(migrations.Migration):
    dependencies = [
        ('astrobin', '0044_use_big_integer_for_data_download_file_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='uncompressed_source_file',
            field=models.FileField(
                help_text='You can store the final processed image that came out of your favorite image editor (e.g. PixInsight, Adobe Photoshop, etc) here on AstroBin, for archival purposes. This file is stored privately and only you will have access to it.',
                max_length=256, null=True, upload_to=astrobin.models.uncompressed_source_upload_path, validators=[
                    common.validators.file_validator.FileValidator(
                        allowed_extensions=(b'xisf', b'fits', b'fit', b'fts', b'psd', b'tiff'))],
                verbose_name='Uncompressed source (max 200 MB)'),
        ),
    ]