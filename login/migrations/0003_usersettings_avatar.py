# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20170310_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='avatar',
            field=models.ImageField(upload_to='/images/', blank=True),
        ),
    ]
