# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-03 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500,
                                           null=True)),
                ('desc', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('image', models.URLField(blank=True, max_length=500,
                                          null=True)),
                ('url', models.URLField(blank=True, max_length=500,
                                        null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
