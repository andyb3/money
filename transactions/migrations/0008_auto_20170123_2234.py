# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 22:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0007_auto_20170123_2233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploaded_file',
            name='upload_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
