# coding=utf-8
from decimal import Decimal
import json
from django.core import urlresolvers
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
import cart
from catalog.models import Product, Category
from utils import promo2


def show_cart(request, promotion_by_code_discount=None):
    if request.method == 'POST':
        post_data = request.POST.copy()
        if 'submit_remove.x' in post_data:
            cart.remove_from_cart(request)
        if 'submit_update.x' in post_data:
            cart.update_cart(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items = cart.get_cart_items(request)

    total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions = promo(request,
                                                                                              promotion_by_code_discount,
                                                                                              cart_item_count,
                                                                                              cart_items)
    print('promo', promotions)
    page_title = 'Shopping Cart'
    return render_to_response('cart/show_cart.html', locals(), context_instance=RequestContext(request))


def add_to_cart_product_list(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        product_slug_list = post_data.getlist('product_slug', [])
        cart.add_to_cart_list_products(request, product_slug_list)
        url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(url)
    return HttpResponseRedirect('/')


def ajax_test(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items = cart.get_cart_items(request)
    real_code = '654321'
    code = request.POST.get('code', '')
    if real_code == code:
        promotion_by_code_discount = 10
        success = 'True'
    else:
        promotion_by_code_discount = None
        success = 'False'
    total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions = promo(request,
                                                                                              promotion_by_code_discount,
                                                                                              cart_item_count,
                                                                                              cart_items)

    resp_dict = {'success': success, 'total': str(total), 'discount': str(discount), 'promotions': promotions,
                 'cart_subtotal': str(cart_subtotal), 'shipping_tax': str(shipping_tax),
                 'shipping_tax_promotions': shipping_tax_promotions}
    response = json.dumps(resp_dict)
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


def promo(request, promotion_by_code_discount, cart_item_count, cart_items):
    discount = Decimal(0.00)
    shipping_tax = Decimal(3.00)
    promotions = False
    # PROMO 3 -- BY CODE DISCOUNT
    cart_subtotal = cart.cart_subtotal(request)
    if promotion_by_code_discount:
        percent = promotion_by_code_discount
        discount = cart_subtotal * percent / 100
        promotions = u"Haz recibido un código de descuento de un {percent}% del total".format(percent=percent)
    # PROMO 2
    if not promotions:
        print(2)
        category, product = promo2()
        style = "<span style='color: #426f42; text-decoration: underline; font-weight: bold;'>"
        promo2_popup = u"Llévate gratis este producto: {style}{product}</span> " \
                       u"si compras dos de esta categoria: {style}{category}</span>".format(style=style,
                                                                                            product=product,
                                                                                            category=category)

        # obtener productos de los cart items
        product_ids = cart_items.values('product')
        product_ids = [product_id['product'] for product_id in product_ids]
        products = Product.active.filter(id__in=product_ids)
        # obtener las categorias de estos prod
        categories = Category.active.filter(product__in=products)
        cant_prod_of_this_cat = list(categories).count(category)
        if cant_prod_of_this_cat == 2:
            if product not in products:
                cart.add_to_cart(request, product)
                discount = product.price
                promotions = promo2_popup
        elif cant_prod_of_this_cat > 2:
            if product not in products:
                cart.add_to_cart(request, product)
            discount = product.price
            promotions = promo2_popup
        cart_subtotal = cart.cart_subtotal(request)

    # PROMO 1 -- 5+ prods
    if cart_item_count >= 5 and not promotions:
        percent = 10  # 10% de descuento
        discount = cart_subtotal * percent / 100
        promotions = "Si llevas 5+ productos te descontamos el 10% del total."

    # PROMO 0 -- SHIPPING TAX
    shipping_tax_promotions = None
    if cart_subtotal >= 75 and not promotions:
        shipping_tax = 0
        shipping_tax_promotions = u"Si compras +75cuc no te cobramos impuestos de envío."
    total = cart_subtotal - discount + shipping_tax
    print('cart-total', total)
    return total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions
