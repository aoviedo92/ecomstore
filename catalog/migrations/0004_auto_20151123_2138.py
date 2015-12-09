# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20151118_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(default=1, max_length=50, choices=[(1, b'Dolce & Gabana'), (2, b'Gucci'), (3, b'Hugo Boss'), (4, b'Versace'), (5, b'Ralph Lauren'), (6, b'Lacoste'), (7, b'Chanel')]),
        ),
    ]
