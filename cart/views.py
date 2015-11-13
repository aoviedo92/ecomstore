from decimal import Decimal
from django.core import urlresolvers
from django.http import HttpResponse, QueryDict, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
import cart
from catalog.models import Product, Category
from utils import promo2


def show_cart(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        print(post_data)
        if 'submit_remove.x' in post_data:
            cart.remove_from_cart(request)
        if 'submit_update.x' in post_data:
            cart.update_cart(request)
    cart_item_count = cart.cart_distinct_item_count(request)
    cart_items = cart.get_cart_items(request)
    # for cart_item in cart_items:
    #     p = cart_item.product
    #     c = p.categories.all()
    #     print('cart - views - categ', c)
    discount = Decimal(0.00)
    shipping_tax = Decimal(3.00)
    promotions = False
    # PROMO 2
    category, product = promo2()
    # obtener productos de los cart items
    product_ids = cart_items.values('product')
    product_ids = [product_id['product'] for product_id in product_ids]
    products = Product.active.filter(id__in=product_ids)
    # obtener las categorias de estos prod
    categories = Category.active.filter(product__in=products)
    cant_prod_of_this_cat = list(categories).count(category)
    if cant_prod_of_this_cat == 2:
        print('cant 2')
        if product not in products:
            print("2 prod != prod")
            cart.add_to_cart(request, product)
            discount = product.price
            promotions = True
    elif cant_prod_of_this_cat > 2:
        print("cant>2")
        if product not in products:
            cart.add_to_cart(request, product)
        discount = product.price
        promotions = True

    cart_subtotal = cart.cart_subtotal(request)

    # PROMO 1
    if cart_item_count >= 5:
        percent = 10  # 10% de descuento
        discount = cart_subtotal * percent / 100
        promotions = True
    if cart_subtotal >= 75 and not promotions:
        shipping_tax = 0
    total = cart_subtotal - discount + shipping_tax
    # print('totla', total)
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
