# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_city',
            field=models.IntegerField(default=0, max_length=50, choices=[(0, b'Seleccione municipio'), (1, b'playa'), (2, b'cerro'), (3, b'lisa'), (4, b'boyeros'), (5, b'plaza'), (6, b'arroyo naranjo'), (7, b'cotorro'), (8, b'marianao'), (9, b'regla'), (10, b'centro habana'), (11, b'habana vieja'), (12, b'habana del este'), (13, b'10 de octubre'), (14, b'guanabacoa'), (15, b'san miguel')]),
        ),
    ]
