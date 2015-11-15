# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20151111_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='catalog.Category', blank=True)),
                ('product', models.ForeignKey(to='catalog.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
