# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_auto_20151203_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=1, null=True, choices=[(1, b'Submitted'), (2, b'Processed'), (3, b'Shipped'), (4, b'Cancelled')]),
        ),
    ]
