# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0007_auto_20170225_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('areaname', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='cafe',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='cafe',
            name='formatted_address',
            field=models.CharField(null=True, max_length=200),
        ),
    ]
