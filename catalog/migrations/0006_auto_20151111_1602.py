# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20151031_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='group',
            field=models.ForeignKey(blank=True, to='catalog.CategoryGroup', null=True),
        ),
    ]
