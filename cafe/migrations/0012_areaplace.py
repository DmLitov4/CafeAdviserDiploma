# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0011_auto_20170225_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Areaplace',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('areaplacename', models.CharField(max_length=30)),
            ],
        ),
    ]
