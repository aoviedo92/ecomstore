# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_promo4_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo4',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
