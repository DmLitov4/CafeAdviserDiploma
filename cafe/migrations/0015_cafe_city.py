# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0014_remove_cafe_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafe',
            name='city',
            field=models.ForeignKey(null=True, to='cafe.Cities'),
        ),
    ]
