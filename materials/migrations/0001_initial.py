# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-23 01:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('color_hex', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.Color')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MaterialType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='material',
            name='material_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.MaterialType'),
        ),
        migrations.AddField(
            model_name='material',
            name='tier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='materials.Size'),
        ),
    ]
