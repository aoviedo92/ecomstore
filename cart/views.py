from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
import cart


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
    cart_subtotal = cart.cart_subtotal(request)
    page_title = 'Shopping Cart'
    return render_to_response('cart/show_cart.html', locals(), context_instance=RequestContext(request))