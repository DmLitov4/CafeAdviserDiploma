# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_cuisine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cafe',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('cuisines', models.ManyToManyField(to='cafe.Cuisine', verbose_name="cafe's cuisines")),
            ],
        ),
        migrations.CreateModel(
            name='Kind',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('kindname', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='cafe',
            name='kind',
            field=models.ForeignKey(to='cafe.Kind'),
        ),
    ]
