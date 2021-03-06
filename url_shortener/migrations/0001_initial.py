# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 00:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('short_id', models.CharField(max_length=12, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')])),
                ('url', models.URLField(max_length=2047)),
                ('added_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date added')),
            ],
        ),
    ]
