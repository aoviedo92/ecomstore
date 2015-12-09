# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_auto_20151203_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ci',
            field=models.CharField(max_length=11, null=True, verbose_name=b'Carnet de identidad', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_city',
            field=models.IntegerField(default=0, max_length=50, verbose_name='Municipio', choices=[(0, b'Seleccione municipio'), (1, b'Playa'), (2, b'Cerro'), (3, b'Lisa'), (4, b'Boyeros'), (5, b'Plaza'), (6, b'Arroyo Naranjo'), (7, b'Cotorro'), (8, b'Marianao'), (9, b'Regla'), (10, b'Centro Habana'), (11, b'Habana Vieja'), (12, b'Habana del Este'), (13, b'10 de Octubre'), (14, b'Guanabacoa'), (15, b'San Miguel')]),
        ),
    ]
