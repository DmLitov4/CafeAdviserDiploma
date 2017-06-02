# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0008_auto_20170225_1306'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Area',
            new_name='Areas',
        ),
        migrations.AddField(
            model_name='cafe',
            name='cafearea',
            field=models.ForeignKey(to='cafe.Areas', null=True),
        ),
        migrations.AddField(
            model_name='cafe',
            name='city',
            field=models.ForeignKey(default=0, to='cafe.Cities'),
        ),
        migrations.AlterField(
            model_name='cafe',
            name='kind',
            field=models.ForeignKey(default=0, to='cafe.Kind'),
        ),
    ]
