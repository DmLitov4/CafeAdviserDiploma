# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_usersettings_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='gender',
            field=models.CharField(default='М', choices=[('М', 'Мужской'), ('Ж', 'Женский')], max_length=2),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='/img/users/'),
        ),
    ]
