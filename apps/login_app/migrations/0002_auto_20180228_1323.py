# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-28 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='state',
            field=models.CharField(max_length=2),
        ),
    ]