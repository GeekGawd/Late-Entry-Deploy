# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-16 07:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filer_gui', '0003_delete_filerguifolder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filerguifile',
            options={'base_manager_name': 'objects'},
        ),
    ]
