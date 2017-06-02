# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0006_auto_20170225_0127'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='bill',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cafe',
            name='parking',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='cafe',
            name='rating',
            field=models.FloatField(null=True),
        ),
    ]
