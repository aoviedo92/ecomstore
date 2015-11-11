# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20151024_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_name',
            field=models.CharField(max_length=50, verbose_name=b'Envio a nombre de'),
        ),
    ]
