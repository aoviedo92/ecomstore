# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from catalog.models import Category
from checkout.models import OrderItem


def sex_summary(request):
    print('here')
    sex_dict = {'0': 0, '1': 0, '2': 0}
    product_ids = [id_['product'] for id_ in OrderItem.objects.values('product')]
    for id_ in product_ids:
        sex = Category.objects.filter(product__id=id_).first().sex
        sex_dict[str(sex)] += 1
    print('sex dict', sex_dict)
    response = json.dumps(sex_dict)
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')



def chart(request):
    return render_to_response('manager/charts.html', {}, context_instance=RequestContext(request))
