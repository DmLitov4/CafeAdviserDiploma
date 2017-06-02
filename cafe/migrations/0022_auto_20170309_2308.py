# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0021_auto_20170309_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='website',
            field=models.CharField(null=True, blank=True, max_length=100),
        ),
    ]
