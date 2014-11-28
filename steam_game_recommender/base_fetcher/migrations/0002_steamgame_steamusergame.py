# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_fetcher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SteamGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('appid', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SteamUserGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game', models.ForeignKey(to='base_fetcher.SteamGame')),
                ('user', models.ForeignKey(to='base_fetcher.SteamUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
