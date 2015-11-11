# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('shipping_name', models.CharField(max_length=50)),
                ('shipping_address_1', models.CharField(max_length=50)),
                ('shipping_address_2', models.CharField(max_length=50, blank=True)),
                ('shipping_city', models.CharField(default=0, max_length=50, choices=[(0, b'Seleccione municipio'), (1, b'playa'), (2, b'cerro'), (3, b'lisa'), (4, b'boyeros'), (5, b'plaza'), (6, b'arroyo naranjo'), (7, b'cotorro'), (8, b'marianao'), (9, b'regla'), (10, b'centro habana'), (11, b'habana vieja'), (12, b'habana del este'), (13, b'10 de octubre'), (14, b'guanabacoa'), (15, b'san miguel')])),
                ('sex', models.CharField(default=0, max_length=15, choices=[(0, b'Seleccione Sexo'), (1, b'Femenino'), (2, b'Masculino')])),
                ('birth_day', models.DateField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
