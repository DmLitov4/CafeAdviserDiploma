# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0020_cafe_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='cuisines',
            field=models.ManyToManyField(null=True, to='cafe.Cuisine', blank=True),
        ),
    ]
