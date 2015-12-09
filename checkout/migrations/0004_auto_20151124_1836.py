# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20151124_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordertotal',
            name='order',
            field=models.OneToOneField(blank=True, to='checkout.Order'),
        ),
    ]
