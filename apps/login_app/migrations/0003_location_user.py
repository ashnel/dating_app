# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-01 01:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0002_auto_20180228_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='location', to='login_app.User'),
            preserve_default=False,
        ),
    ]