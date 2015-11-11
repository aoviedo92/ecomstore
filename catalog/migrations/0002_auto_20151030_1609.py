# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField(default=5, choices=[(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)])),
                ('is_approved', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('product', models.ForeignKey(to='catalog.Product')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='product',
            name='details',
        ),
        migrations.RemoveField(
            model_name='product',
            name='more_info',
        ),
    ]
