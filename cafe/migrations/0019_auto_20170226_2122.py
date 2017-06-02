# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0018_auto_20170226_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='photos',
            field=models.ManyToManyField(to='cafe.Photo', blank=True),
        ),
    ]
