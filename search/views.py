from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from catalog.product_list import __get_num_x_pag_session, order_products, get_num_x_pag, get_paginator, filter_products
import search
from ecomstore import settings
from stats import stats
from utils import get_product_row


def results(request):
    # get current search phrase
    q = request.GET.get('q', '')

    matching = search.products(q)
    if q:
        request.session['search_key'] = q

    # num_x_pag_session = get_num_x_pag_session(request)

    products, order_by_form = order_products(request, matching)

    num_x_pag, product_per_pag_form = get_num_x_pag(request)
    products, order_by_brand_form = filter_products(request, products)
    paginator, products_per_pag = get_paginator(request, products, num_x_pag)

    product_row = get_product_row(products_per_pag)

    search.store(request, q, matching)
    print("s",request.session['search_key'])
    page_title = 'Search Results for: ' + q
    return render_to_response("tags/product_list.html", locals(), context_instance=RequestContext(request))
