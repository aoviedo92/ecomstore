# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20151030_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='title',
        ),
        migrations.AlterField(
            model_name='productreview',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
