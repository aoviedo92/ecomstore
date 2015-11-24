# coding=utf-8
from django.contrib.auth.views import logout
from catalog.product_list import order_products, get_num_x_pag, get_paginator, filter_products
from models import UserProfile
import profile
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from forms import UserProfileForm, UserCreationForm
from checkout.models import Order, OrderItem
from utils import get_product_row, get_discount_code
from manager.models import Promo3, Promo4


def register(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserCreationForm(postdata)
        if form.is_valid():
            form.save()
            un = postdata.get('username', '')
            pw = postdata.get('password1', '')
            from django.contrib.auth import login, authenticate

            new_user = authenticate(username=un, password=pw)
            if new_user and new_user.is_active:
                login(request, new_user)
                url = urlresolvers.reverse('my_account')
                return HttpResponseRedirect(url)
    else:
        form = UserCreationForm()
    page_title = 'User Registration'
    return render_to_response("registration/register.html", locals(), context_instance=RequestContext(request))


@login_required
def my_account(request):
    page_title = 'My Account'
    orders = Order.objects.filter(user=request.user)
    name = request.user.username
    promo4 = Promo4.objects.filter(winner_user=request.user, active=True).first()  # siempre sera uno solo
    products_chain = ''
    if promo4:
        for product in promo4.products.all():
            products_chain += unicode(product) + '<br/>'
        small_text = "Ud. ha sido el ganador de una rifa, y ahora puede comprar estos productos:<br/>" + products_chain
        print(small_text)
        big_text = "por un descuento del %d%%" % promo4.discount
    else:
        code, discount_ = get_discount_code(request)
        small_text = u"Haz recibido un código de descuento! úsalo en el carrito de la compra. %s%%" % discount_
        big_text = code
    return render_to_response("registration/my_account.html", locals(), context_instance=RequestContext(request))


@login_required
def order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    page_title = 'Order Details for Order #' + order_id
    order_items = OrderItem.objects.filter(order=order)
    status_dict = {1: u'Su petición ha sido enviada', 2: 'La orden ha sido procesada',
                   3: 'La orden ha sido enviada al cliente', 4: 'La orden ha sido cancelada'}
    status = status_dict[order.status]
    return render_to_response("registration/order_details.html", locals(), context_instance=RequestContext(request))


@login_required
def order_info(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        form = UserProfileForm(post_data)
        if form.is_valid():
            profile.set_profile(request)
            url = urlresolvers.reverse('my_account')
            return HttpResponseRedirect(url)
    else:
        # user_profile = UserProfile(user=request.user)
        user_profile = profile.get_profile(request)
        print('account - order_info - userprofile', user_profile)
        form = UserProfileForm(instance=user_profile)
    envio = u"envío"
    info = u"información"
    page_title = 'Edit Order Information'
    return render_to_response("registration/order_info.html", locals(), context_instance=RequestContext(request))


@login_required()
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required
def wish_list(request):
    user_profile = profile.get_profile(request)
    products = user_profile.wish_list.all()
    title_head = "Tu lista de deseos"
    if products:
        products, order_by_form = order_products(request, products)
        num_x_pag, product_per_pag_form = get_num_x_pag(request)
        products, order_by_brand_form = filter_products(request, products)
        paginator, products_per_pag = get_paginator(request, products, num_x_pag)
        show_toolbar = True
    else:
        show_toolbar = False
        paginator, products_per_pag = get_paginator(request, [], 1)
    product_row = get_product_row(products_per_pag)

    return render_to_response("tags/product_list.html", locals(), context_instance=RequestContext(request))
