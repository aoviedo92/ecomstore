# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_ordertotal_purchased'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_total',
        ),
        migrations.AddField(
            model_name='ordertotal',
            name='order',
            field=models.OneToOneField(null=True, blank=True, to='checkout.Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ordertotal',
            name='promo',
            field=models.CharField(default=b'no', max_length=50),
            preserve_default=True,
        ),
    ]
