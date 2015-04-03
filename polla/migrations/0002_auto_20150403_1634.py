# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.sites.models


class Migration(migrations.Migration):

    dependencies = [
        ('polla', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitealias',
            name='domain',
            field=models.CharField(max_length=100, validators=[django.contrib.sites.models._simple_domain_name_validator], unique=True, verbose_name='domain name alias'),
        ),
    ]
