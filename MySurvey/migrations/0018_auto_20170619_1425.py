# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-19 19:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kibosurvey', '0017_auto_20170607_1523'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Employee',
        ),
        migrations.AddField(
            model_name='profile',
            name='password',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]