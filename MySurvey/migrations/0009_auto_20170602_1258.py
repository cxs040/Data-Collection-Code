# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-02 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kibosurvey', '0008_profile_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='question',
        ),
        migrations.AddField(
            model_name='rating',
            name='question',
            field=models.ManyToManyField(to='kibosurvey.Question'),
        ),
    ]
