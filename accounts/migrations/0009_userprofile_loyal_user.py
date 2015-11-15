# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20151109_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='loyal_user',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
