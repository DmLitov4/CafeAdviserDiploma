# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0010_auto_20170225_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='cafearea',
        ),
        migrations.DeleteModel(
            name='Areas',
        ),
    ]
