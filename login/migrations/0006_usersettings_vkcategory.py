# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20170315_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='vkcategory',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
