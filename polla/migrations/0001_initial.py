# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.sites.models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100, verbose_name='domain name alias')),
                ('site', models.ForeignKey(related_name='aliases', verbose_name='site', to='sites.Site')),
            ],
            options={
                'verbose_name_plural': 'SiteAliases',
                'verbose_name': 'SiteAlias',
            },
        ),
    ]
