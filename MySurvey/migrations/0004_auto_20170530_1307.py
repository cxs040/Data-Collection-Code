# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-30 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kibosurvey', '0003_remove_question_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='employee_password',
            field=models.CharField(default=12345, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_username',
            field=models.CharField(default=12345, max_length=200),
            preserve_default=False,
        ),
    ]
