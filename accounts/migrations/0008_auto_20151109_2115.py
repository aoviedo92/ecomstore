# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20151109_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.IntegerField(default=0, max_length=15, choices=[(0, b'Seleccione Sexo'), (1, b'Femenino'), (2, b'Masculino')]),
        ),
    ]
