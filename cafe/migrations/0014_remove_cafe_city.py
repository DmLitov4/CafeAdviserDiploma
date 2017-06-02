# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0013_cafe_areaplace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cafe',
            name='city',
        ),
    ]
