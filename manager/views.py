# coding=utf-8
from decimal import Decimal
import glob
import json
from random import randint
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from accounts.models import UserProfile
from catalog.models import CategoryGroup, CommonCategory, Category, Product
from manager.models import Promo3, Promo4
from utils import generate_random_id


def test_superuser(user):
    return user.is_superuser

@user_passes_test(test_superuser, login_url='/admin/')
def dashboard(request):
    return render_to_response('manager/analytics.html', {}, context_instance=RequestContext(request))


@user_passes_test(test_superuser)
def create_group_categories(request):
    """
    autopopulate las categorias
    """
    group = ["Hombres", "Mujeres", "Bodas", "Tejidos", "Uniformes"]
    for group_name in group:
        CategoryGroup.objects.create(group_name=group_name)
    commons = ['Accesorios', 'Conjuntos', 'Carteras', 'Blusas', u'Bañadores']
    for common in commons:
        CommonCategory.objects.create(common_name=common)
    Category.objects.create(name='Trajes para hombres', slug='trajes-para-hombres',
                            group=CategoryGroup.objects.get(group_name='Bodas'), sex=2)
    Category.objects.create(name='Trajes para mujeres', slug='trajes-para-mujeres',
                            group=CategoryGroup.objects.get(group_name='Bodas'), sex=1)
    Category.objects.create(name='Abrigos', slug='abrigos', group=CategoryGroup.objects.get(group_name='Hombres'),
                            sex=2)
    Category.objects.create(name='Jeans', slug='jeans', group=CategoryGroup.objects.get(group_name='Hombres'), sex=2)
    Category.objects.create(name='Pulovers', slug='pulovers', group=CategoryGroup.objects.get(group_name='Hombres'),
                            sex=2)
    Category.objects.create(name='Conjuntos para hombres', slug=slugify('Conjuntos para hombres'),
                            common=CommonCategory.objects.get(common_name="Conjuntos"),
                            group=CategoryGroup.objects.get(group_name='Hombres'), sex=2)
    Category.objects.create(name='Conjuntos para mujeres', slug=slugify('Conjuntos para mujeres'),
                            common=CommonCategory.objects.get(common_name="Conjuntos"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Accesorios para mujeres', slug=slugify('Accesorios para mujeres'),
                            common=CommonCategory.objects.get(common_name="Accesorios"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Blusas para mujeres', slug=slugify('Blusas para mujeres'),
                            common=CommonCategory.objects.get(common_name="Blusas"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Carteras para mujeres', slug=slugify('Carteras para mujeres'),
                            common=CommonCategory.objects.get(common_name="Carteras"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name=u'Bañadores para mujeres', slug=slugify(u'Bañadores para mujeres'),
                            common=CommonCategory.objects.get(common_name=u"Bañadores"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name=u'Gafas', slug=slugify(u'Gafas'),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name=u'Vestidos', slug=slugify(u'Vestidos'),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Accesorios tejidos', slug=slugify('Accesorios tejidos'),
                            common=CommonCategory.objects.get(common_name="Accesorios"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name='Blusas tejidas', slug=slugify('Blusas tejidas'),
                            common=CommonCategory.objects.get(common_name="Blusas"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name='Carteras tejidas', slug=slugify('Carteras tejidas'),
                            common=CommonCategory.objects.get(common_name="Carteras"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name=u'Bañadores tejidos', slug=slugify(u'Bañadores tejidos'),
                            common=CommonCategory.objects.get(common_name=u"Bañadores"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name=u'Bebé', slug=slugify(u'Bebé'), group=CategoryGroup.objects.get(group_name='Tejidos'),
                            sex=1)
    Category.objects.create(name='Uniformes para hombres', slug='uniformes-para-hombres',
                            group=CategoryGroup.objects.get(group_name='Uniformes'), sex=2)
    Category.objects.create(name='Uniformes para mujeres', slug='uniformes-para-mujeres',
                            group=CategoryGroup.objects.get(group_name='Uniformes'), sex=1)

@user_passes_test(test_superuser)
def create_products(request):
    category_list = Category.objects.all()
    for category in category_list:
        try:
            create_product_aux(category)
        except:
            pass
    return HttpResponse()


def create_product_aux(category):
    cant = randint(7, 10)
    cent_list = [00, 05, 15, 25, 35, 45, 55, 65, 75, 85, 95]  # la parte de los centavos $xx.95
    for i in range(0, cant):
        name = '%s %d' % (category.name, i)
        image = 'image%d' % i
        doll = randint(10, 50)
        cent = cent_list[randint(0, len(cent_list) - 1)]
        price = Decimal('%d.%d' % (doll, cent))
        product = Product.objects.create(name=name, slug=slugify(name), image=image, price=price)
        product.categories.add(category)
        product.save()



