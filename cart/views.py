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
from checkout.models import Order, OrderTotal
from manager.models import Promo3
from utils import promo2, get_discount_code


def show_cart(request, promotion_by_code_discount=None):
    # try:
    #     del request.session['promo3_id']
    # except KeyError:
    #     pass
    if request.method == 'POST':
        post_data = request.POST.copy()
        if 'submit_remove.x' in post_data:
            cart.remove_from_cart(request)
        if 'submit_update.x' in post_data:
            cart.update_cart(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items = cart.get_cart_items(request)

    code, discount_ = get_discount_code(request)
    small_text = u"Puedes usar tu código de descuento aquí. %s" % discount_
    big_text = code

    total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions = promo(request,
                                                                                              promotion_by_code_discount,
                                                                                              cart_item_count,
                                                                                              cart_items)
    # request.session['total'] = str(total)
    # print('cook total - views',request.session['total'])
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


def ajax_promo3(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items = cart.get_cart_items(request)
    # ver si este usuario tiene asignado un codigo de descuento.
    try:
        promo3 = Promo3.objects.get(user=request.user)
        real_code = promo3.code
        code = request.POST.get('code', '')
        if real_code == code:
            promotion_by_code_discount = promo3.discount
            success = 'True'
            request.session['promo3_id'] = str(promo3.id)
        else:
            promotion_by_code_discount = None
            success = 'False'
    except Promo3.DoesNotExist:
        success = 'False'
        promotion_by_code_discount = None
    total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions = promo(request,
                                                                                              promotion_by_code_discount,
                                                                                              cart_item_count,
                                                                                              cart_items)

    resp_dict = {'success': success, 'total': '$%.2f' % total, 'discount': '$%.2f' % discount, 'promotions': promotions,
                 'cart_subtotal': '$%.2f' % cart_subtotal, 'shipping_tax': '$%.2f' % shipping_tax,
                 'shipping_tax_promotions': shipping_tax_promotions}
    response = json.dumps(resp_dict)
    # request.session['total'] = str(total)
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
    # PROMO 2 -- llevate gratis <P> si compras 2 de <C>
    if not promotions:
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

    total = create_order_step_1(request, cart_subtotal, discount, shipping_tax)
    print('cart-total', total)
    total = Decimal('%.2f' % total)
    discount = Decimal('%.2f' % discount)
    discount = Decimal('%.2f' % discount)
    cart_subtotal = Decimal('%.2f' % cart_subtotal)
    shipping_tax = Decimal('%.2f' % shipping_tax)
    return total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions


def create_order_step_1(request, cart_subtotal, discount, shipping_tax):
    try:
        del request.session['ordertotalid']
    except KeyError:
        pass
    total = cart_subtotal - discount + shipping_tax
    order_total = OrderTotal.objects.create(shipping_tax=shipping_tax, discount=discount, cart_subtotal=cart_subtotal)
    order_total.save()
    request.session['ordertotalid'] = order_total.id
    print('order-total', order_total)

    return total
