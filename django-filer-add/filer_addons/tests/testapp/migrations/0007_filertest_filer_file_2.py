# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-07 05:29
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import filer_addons.filer_gui.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0007_auto_20161016_1055'),
        ('testapp', '0006_fileruglytest'),
    ]

    operations = [
        migrations.AddField(
            model_name='filertest',
            name='filer_file_2',
            field=filer_addons.filer_gui.fields.FilerFileField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file2_filertest', to='filer.File'),
        ),
    ]
