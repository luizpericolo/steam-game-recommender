# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_fetcher', '0003_auto_20141128_0210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steamusergame',
            name='total_minutes_played',
        ),
        migrations.AddField(
            model_name='steamusergame',
            name='total_hours_played',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
    ]
