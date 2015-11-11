# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_userprofile_birth_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='shipping_name',
            field=models.CharField(max_length=50, verbose_name=b'Envio a nombre de'),
        ),
    ]
