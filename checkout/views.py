from decimal import Decimal
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from accounts import profile
from accounts.models import UserProfile
from forms import CheckoutForm
from manager.models import Promo3
from models import Order, OrderItem, OrderTotal
import checkout
from cart import cart


def show_checkout(request):
    if cart.is_empty(request):
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)

    if request.method == 'POST':
        post_data = request.POST.copy()
        form = CheckoutForm(post_data)
        if form.is_valid():
            response = checkout.process(request)
            order_number = response.get('order_number', 0)
            error_message = response.get('message', '')
            if order_number:
                request.session['order_number'] = order_number
                receipt_url = urlresolvers.reverse('checkout_receipt')
                return HttpResponseRedirect(receipt_url)
        else:
            error_message = 'Corrige los errores abajo'
    else:
        # si la peticion es get, tratar de vincular el form con los datos del perfil del usuario
        if request.user.is_authenticated():
            user_profile = profile.get_profile(request)
            form = CheckoutForm(instance=user_profile, label_suffix="")
        else:
            form = CheckoutForm(label_suffix="")
    page_title = 'Checkout'
    small_text = u"Total en el carrito"
    big_text = "%.2fcuc" % OrderTotal.objects.get(id=request.session['ordertotalid']).total
    return render_to_response('checkout/checkout.html', locals(), context_instance=RequestContext(request))


def receipt(request):
    order_number = request.session.get('order_number', '')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session['order_number']
    else:
        cart_url = urlresolvers.reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    return render_to_response('checkout/receipt.html', locals(), context_instance=RequestContext(request))
