# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-02 08:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recommendations', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductPairOccurrences',
            new_name='ProductPairOccurrence',
        ),
    ]
