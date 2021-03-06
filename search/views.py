from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from catalog.product_list import __get_num_x_pag_session, order_products, get_num_x_pag, get_paginator, filter_products
import search
from ecomstore import settings
from stats import stats
from utils import get_product_row
from django.core.cache import cache


def results(request):
    # get current search phrase
    q = request.GET.get('q', '')

    if q:
        request.session['search_key'] = q
    else:
        q = request.session.get('search_key', '')
    cache_key = 'search_cache' + q
    matching = cache.get(cache_key)
    if not matching:
        matching = search.products(q)
        cache.set(cache_key, matching, settings.CACHE_TIMEOUT)
    if matching:
        products, order_by_form = order_products(request, matching)
        num_x_pag, product_per_pag_form = get_num_x_pag(request)
        products, order_by_brand_form = filter_products(request, products)
        paginator, products_per_pag = get_paginator(request, products, num_x_pag)
        show_toolbar = True
    else:
        show_toolbar = False
        paginator, products_per_pag = get_paginator(request, [], 1)

    product_row = get_product_row(products_per_pag)

    search.store(request, q, matching)
    page_title = 'Search Results for: ' + q
    title_head = "Resultados"
    return render_to_response("tags/product_list.html", locals(), context_instance=RequestContext(request))
