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
from manager.models import Promo3, Promo4
from utils import promo2, get_discount_code



def show_cart(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        if 'submit_remove.x' in post_data:
            cart.remove_from_cart(request)
        if 'submit_update.x' in post_data:
            cart.update_cart(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items = cart.get_cart_items(request)
    # mostrar el panel amarillo con infos muy importantes(1 de solo 2)
    if request.user.is_authenticated():
        try:
            promo4 = Promo4.objects.get(winner_user=request.user, active=True)
            small_text = "Ud. ha sido el ganador de una rifa, y ahora puede comprar estos productos<br/>"
            big_text = "Por un descuento del %d%%" % promo4.discount
        except Promo4.DoesNotExist:
            code, discount_ = get_discount_code(request)
            small_text = u"Puedes usar tu código de descuento aquí. %s%%" % discount_
            big_text = code

    total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions = promo(request,
                                                                                              cart_item_count,
                                                                                              cart_items)
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
                                                                                              cart_item_count,
                                                                                              cart_items,
                                                                                              promotion_by_code_discount=promotion_by_code_discount
                                                                                              )

    resp_dict = {'success': success, 'total': '$%.2f' % total, 'discount': '$%.2f' % discount, 'promotions': promotions,
                 'cart_subtotal': '$%.2f' % cart_subtotal, 'shipping_tax': '$%.2f' % shipping_tax,
                 'shipping_tax_promotions': shipping_tax_promotions}
    response = json.dumps(resp_dict)
    # request.session['total'] = str(total)
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


def promo(request, cart_item_count, cart_items, promotion_by_code_discount=None):
    discount, promotions, promo_label_for_db = anonymous_user(request)
    if not promotions:
        discount, promotions, promo_label_for_db = promo4_rifas(request, cart_items)
    if not promotions:
        discount, promotions, promo_label_for_db = promo3_code_discount(request, promotion_by_code_discount)
    if not promotions:
        discount, promotions, promo_label_for_db = promo2_buy_two_take_one(request, cart_items)
    if not promotions:
        discount, promotions, promo_label_for_db = promo1_more_5_prods(request, cart_item_count)
    shipping_tax, shipping_tax_promotions = promo0_shipping_tax(request, promotions)
    if shipping_tax_promotions:
        promo_label_for_db = 'shipping_tax'
    cart_subtotal = cart.cart_subtotal(request)
    cart_subtotal = Decimal('%.2f' % cart_subtotal)
    discount = Decimal('%.2f' % discount)
    shipping_tax = Decimal('%.2f' % shipping_tax)
    total = create_order_step_1(request, cart_subtotal, discount, shipping_tax, promo_label_for_db)
    total = Decimal('%.2f' % total)
    return total, discount, promotions, cart_subtotal, shipping_tax, shipping_tax_promotions


def anonymous_user(request):
    if request.user.is_anonymous():
        discount = 0.00
        promotions = u"Convirtiéndote en usuario de nuestro sitio podrías obtener numerosas ventajas a la hora de la compra y también generosos descuentos!"
        return discount, promotions, 'no'
    return 0.00, False, 'no'


def promo4_rifas(request, cart_items):
    if request.user.is_authenticated():
        promo4 = Promo4.objects.filter(winner_user=request.user, active=True).first()
        if promo4:
            request.session['promo4_id'] = str(promo4.id)

            total = Decimal(0.00)
            cart_items_products = cart.get_product_from_cart_item(cart_items)
            for product in promo4.products.all():
                if product not in cart_items_products:
                    cart.add_to_cart(request, product)
                total += product.price
            percent = promo4.discount
            discount = total * percent / 100
            promotions = "Ud. ha sido el ganador de una rifa, y ahora puede comprar estos productos " \
                         "por un descuento del %d%%" % percent
            return discount, promotions, 'rifas'
    return 0.00, False, 'no'


def promo3_code_discount(request, promotion_by_code_discount):
    cart_subtotal = cart.cart_subtotal(request)
    if promotion_by_code_discount:
        percent = promotion_by_code_discount
        discount = cart_subtotal * percent / 100
        promotions = u"Haz recibido un código de descuento de un {percent}% del total".format(percent=percent)
        return discount, promotions, 'code_discount'
    return 0.00, False, 'no'


def promo2_buy_two_take_one(request, cart_items):
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
    if cant_prod_of_this_cat >= 2:
        if product not in products:
            cart.add_to_cart(request, product)
        discount = product.price
        promotions = promo2_popup
        return discount, promotions, "buy_two_take_one"
    return 0.00, False, 'no'


def promo1_more_5_prods(request, cart_item_count):
    if cart_item_count >= 5:
        cart_subtotal = cart.cart_subtotal(request)
        percent = 10  # 10% de descuento
        discount = cart_subtotal * percent / 100
        promotions = "Si llevas 5+ productos te descontamos el 10% del total."
        return discount, promotions, 'more_5_prods'
    return 0.00, False, 'no'


def promo0_shipping_tax(request, promotions):
    cart_subtotal = cart.cart_subtotal(request)
    if cart_subtotal >= 75 and request.user.is_authenticated() and not promotions:
        shipping_tax = 0
        shipping_tax_promotions = u"Si compras +75cuc no te cobramos impuestos de envío."
        return shipping_tax, shipping_tax_promotions
    return 3.00, False


def create_order_step_1(request, cart_subtotal, discount, shipping_tax, shipping_tax_promotions):
    total = cart_subtotal - discount + shipping_tax
    try:
        order_total_id = request.session['ordertotalid']
        order_total = OrderTotal.objects.get(id=order_total_id)
        order_total.shipping_tax = shipping_tax
        order_total.discount = discount
        order_total.cart_subtotal = cart_subtotal
        order_total.promo = shipping_tax_promotions
        order_total.save()
    except KeyError:
        order_total = OrderTotal()
        order_total.shipping_tax = shipping_tax
        order_total.discount = discount
        order_total.cart_subtotal = cart_subtotal
        order_total.promo = shipping_tax_promotions
        order_total.save()
        request.session['ordertotalid'] = order_total.id
    return total
