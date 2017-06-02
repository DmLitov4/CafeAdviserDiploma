# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_auto_20170224_2022'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Area',
        ),
        migrations.RemoveField(
            model_name='cafe',
            name='rating',
        ),
    ]
