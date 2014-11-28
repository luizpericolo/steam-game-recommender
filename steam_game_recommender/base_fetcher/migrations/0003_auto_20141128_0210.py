# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_fetcher', '0002_steamgame_steamusergame'),
    ]

    operations = [
        migrations.AddField(
            model_name='steamusergame',
            name='achievements_percentage',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='steamusergame',
            name='total_minutes_played',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
