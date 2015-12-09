# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0012_remove_order_ci'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ci',
            field=models.CharField(default=b'123', max_length=11, verbose_name=b'Carnet de identidad'),
            preserve_default=True,
        ),
    ]
