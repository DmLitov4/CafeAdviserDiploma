# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='cuisines',
            field=models.ManyToManyField(to='cafe.Cuisine'),
        ),
    ]
