# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20151024_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='birth_day',
        ),
    ]
