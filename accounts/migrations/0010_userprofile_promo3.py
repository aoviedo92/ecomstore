# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
        ('accounts', '0009_userprofile_loyal_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='promo3',
            field=models.OneToOneField(null=True, blank=True, to='manager.Promo3'),
            preserve_default=True,
        ),
    ]
