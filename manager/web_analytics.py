# -*- coding: utf-8 -*-
import json
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from catalog.models import Category, Product
from checkout.models import OrderItem, Order


def test_superuser(user):
    return user.is_superuser


@user_passes_test(test_superuser)
def sex_summary(request):
    """
    ropa vendida por sexo de prenda.
    0- ambos, 1-mujeres, 2-hombres
    """
    sex_dict_buy = {'0': 0, '1': 0, '2': 0}
    sex_dict_all = {'0': 0, '1': 0, '2': 0}
    product_ids = [id_['product'] for id_ in OrderItem.objects.values('product')]
    for id_ in product_ids:
        sex = Category.active.filter(product__id=id_).first().sex
        sex_dict_buy[str(sex)] += 1
    for product in Product.active.all():
        sex = product.categories.first().sex
        sex_dict_all[str(sex)] += 1
    response = json.dumps([sex_dict_buy, sex_dict_all])
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@user_passes_test(test_superuser)
def buy_month(request):
    """
    resumen mensual por ventas
    """
    months_dict = {}
    months = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    months_nums = range(1, 13)
    for month, nums in zip(months, months_nums):
        orders = Order.objects.filter(last_updated__month=nums)
        if orders:
            for order in orders:
                try:
                    months_dict[month] += int(order.ordertotal.total)
                except KeyError:
                    months_dict[month] = int(order.ordertotal.total)
        else:
            months_dict[month] = 0
    print(months_dict)
    response = json.dumps(months_dict)
    print(response)
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


def chart(request):
    return render_to_response('manager/charts.html', {}, context_instance=RequestContext(request))
