# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20151117_1701'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='promo2',
            name='category',
        ),
        migrations.RemoveField(
            model_name='promo2',
            name='product',
        ),
        migrations.DeleteModel(
            name='Promo2',
        ),
    ]
