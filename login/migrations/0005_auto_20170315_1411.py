# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0022_auto_20170309_2308'),
        ('login', '0004_auto_20170310_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersettings',
            name='liked',
            field=models.ManyToManyField(blank=True, null=True, to='cafe.Cafe'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users/'),
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='gender',
            field=models.CharField(default='М', choices=[('М', 'Мужской'), ('Ж', 'Женский')], max_length=1),
        ),
    ]
