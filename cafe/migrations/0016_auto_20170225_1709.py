# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0015_cafe_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='areaplace',
            field=models.ForeignKey(to='cafe.Areaplace', null=True),
        ),
    ]
