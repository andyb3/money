# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 17:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20170113_1720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='typeID',
            new_name='tx_type',
        ),
    ]
