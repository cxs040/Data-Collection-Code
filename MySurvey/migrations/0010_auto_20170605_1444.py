# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-05 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kibosurvey', '0009_auto_20170602_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id_number', models.IntegerField(default=0)),
                ('question_number', models.IntegerField(default=0)),
                ('rating_number', models.IntegerField(default=0)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user_group',
        ),
        migrations.RemoveField(
            model_name='question',
            name='product',
        ),
        migrations.AddField(
            model_name='question',
            name='product',
            field=models.ManyToManyField(to='kibosurvey.Product'),
        ),
        migrations.AddField(
            model_name='results',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kibosurvey.Profile'),
        ),
    ]