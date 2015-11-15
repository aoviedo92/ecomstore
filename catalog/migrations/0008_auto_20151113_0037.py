# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_promo2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo2',
            name='category',
            field=models.ForeignKey(blank=True, to='catalog.Category', null=True),
        ),
    ]
