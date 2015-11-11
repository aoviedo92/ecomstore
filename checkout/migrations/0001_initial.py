# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('shipping_name', models.CharField(max_length=50)),
                ('shipping_address_1', models.CharField(max_length=50)),
                ('shipping_address_2', models.CharField(max_length=50, blank=True)),
                ('shipping_city', models.CharField(default=0, max_length=50, choices=[(0, b'Seleccione municipio'), (1, b'playa'), (2, b'cerro'), (3, b'lisa'), (4, b'boyeros'), (5, b'plaza'), (6, b'arroyo naranjo'), (7, b'cotorro'), (8, b'marianao'), (9, b'regla'), (10, b'centro habana'), (11, b'habana vieja'), (12, b'habana del este'), (13, b'10 de octubre'), (14, b'guanabacoa'), (15, b'san miguel')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Submitted'), (2, b'Processed'), (3, b'Shipped'), (4, b'Cancelled')])),
                ('ip_address', models.IPAddressField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('transaction_id', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(max_digits=9, decimal_places=2)),
                ('order', models.ForeignKey(to='checkout.Order')),
                ('product', models.ForeignKey(to='catalog.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
