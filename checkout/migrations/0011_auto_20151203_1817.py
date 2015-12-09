# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0010_auto_20151203_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ci',
            field=models.CharField(max_length=11, null=True, verbose_name=b'Carnet de identidad', blank=True),
        ),
    ]
