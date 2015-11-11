# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20151030_1609'),
        ('accounts', '0005_auto_20151026_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wish_list',
            field=models.ManyToManyField(to='catalog.Product', blank=True),
            preserve_default=True,
        ),
    ]
