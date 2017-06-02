# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0009_auto_20170225_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='city',
            field=models.ForeignKey(to='cafe.Cities'),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='kind',
            field=models.ForeignKey(to='cafe.Kind'),
        ),
    ]
