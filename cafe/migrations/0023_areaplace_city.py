# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0022_auto_20170309_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='areaplace',
            name='city',
            field=models.ForeignKey(to='cafe.Cities', null=True),
        ),
    ]
