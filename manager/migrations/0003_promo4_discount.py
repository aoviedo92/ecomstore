# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_promo2_promo4'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo4',
            name='discount',
            field=models.IntegerField(default=40),
            preserve_default=True,
        ),
    ]
