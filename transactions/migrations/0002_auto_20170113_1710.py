# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-13 17:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ofx_upload',
            old_name='account',
            new_name='accountID',
        ),
    ]
