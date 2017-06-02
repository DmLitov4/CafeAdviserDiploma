# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0019_auto_20170226_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='website',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
