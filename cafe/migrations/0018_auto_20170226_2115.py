# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0017_auto_20170225_1713'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photourl', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='cafe',
            name='photos',
            field=models.ManyToManyField(to='cafe.Photo'),
        ),
    ]
