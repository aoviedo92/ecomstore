# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_auto_20151124_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertotal',
            name='order',
            field=models.OneToOneField(null=True, blank=True, to='checkout.Order'),
        ),
    ]
