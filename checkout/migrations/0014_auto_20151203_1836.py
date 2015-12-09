# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0013_order_ci'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ci',
            field=models.CharField(default=b'', max_length=11, verbose_name=b'Carnet de identidad'),
        ),
    ]
