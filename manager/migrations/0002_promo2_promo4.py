# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20151118_1131'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promo2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(blank=True, to='catalog.Category', null=True)),
                ('product', models.ForeignKey(to='catalog.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Promo4',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valid_until', models.DateField()),
                ('products', models.ManyToManyField(to='catalog.Product')),
                ('users', models.ManyToManyField(related_name=b'usuarios inscritos', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
                ('winner_user', models.ForeignKey(related_name=b'usuario ganador', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
