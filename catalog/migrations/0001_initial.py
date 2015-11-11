# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('sex', models.IntegerField(default=0, choices=[(0, b'Ambos'), (1, b'Femenino'), (2, b'Masculino')])),
            ],
            options={
                'db_table': 'categories',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommonCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('common_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'images/products/secondary')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('brand', models.CharField(default=b'brand', max_length=50)),
                ('sku', models.CharField(default=b'sku', max_length=50)),
                ('price', models.DecimalField(default=200, max_digits=9, decimal_places=2)),
                ('old_price', models.DecimalField(default=0.0, max_digits=9, decimal_places=2, blank=True)),
                ('image', models.ImageField(upload_to=b'images/products/main')),
                ('is_active', models.BooleanField(default=True)),
                ('is_bestseller', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=30)),
                ('description', models.TextField(default=b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy\n                            nibh\n                            euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim\n                            veniam,\n                            quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo\n                            consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie\n                            consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto\n                            odio\n                            dignissim qui blandit')),
                ('details', models.TextField(default=b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy\n                            nibh\n                            euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim\n                            veniam,\n                            quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo\n                            consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie\n                            consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto\n                            odio\n                            dignissim qui blandit', null=True, blank=True)),
                ('more_info', models.TextField(default=b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy\n                            nibh\n                            euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim\n                            veniam,\n                            quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo\n                            consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie\n                            consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto\n                            odio\n                            dignissim qui blandit', null=True, blank=True)),
                ('meta_keywords', models.CharField(default=b'meta', help_text=b'Comma-delimited set of SEO keywords for meta tag', max_length=255)),
                ('meta_description', models.CharField(default=b'meta', help_text=b'Content for description meta tag', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(to='catalog.Category')),
                ('second_images', models.ManyToManyField(to='catalog.Images', null=True, blank=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'db_table': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='category',
            name='common',
            field=models.ForeignKey(blank=True, to='catalog.CommonCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='category',
            name='group',
            field=models.ForeignKey(to='catalog.CategoryGroup', null=True),
            preserve_default=True,
        ),
    ]
