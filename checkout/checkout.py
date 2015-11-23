from decimal import Decimal
from cart import cart
from forms import CheckoutForm
from manager.models import Promo3, Promo4
from models import Order, OrderItem, OrderTotal


def do_auth_capture(amount="0.00", card_num=None, exp_date=None, card_cvv=None):
    """
    procesar los datos consumiendo algun servicio.
    """
    response_code = '1'
    transaction_id = 'trans_ID'
    return [response_code, 0, 0, 0, 0, 0, transaction_id]


def process(request):
    # Transaction results
    APPROVED = '1'
    DECLINED = '2'
    ERROR = '3'
    HELD_FOR_REVIEW = '4'
    postdata = request.POST.copy()
    card_num = postdata.get('credit_card_number', '')
    exp_month = postdata.get('credit_card_expire_month', '')
    exp_year = postdata.get('credit_card_expire_year', '')
    exp_date = exp_month + exp_year
    cvv = postdata.get('credit_card_cvv', '')
    # amount = cart.cart_subtotal(request)
    # order_total_id = 1
    order_total_id = request.session['ordertotalid']
    order_total = OrderTotal.objects.get(id=order_total_id)
    amount = order_total.total
    del request.session['ordertotalid']

    results = {}
    response = do_auth_capture(amount=amount,
                               card_num=card_num,
                               exp_date=exp_date,
                               card_cvv=cvv)
    if response[0] == APPROVED:
        transaction_id = response[6]
        order = create_order(request, order_total, transaction_id)
        # order = create_order(request, transaction_id)
        results = {'order_number': order.id, 'message': ''}
    if response[0] == DECLINED:
        results = {'order_number': 0, 'message': 'There is a problem with your credit card.'}
    if response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
        results = {'order_number': 0, 'message': 'Error processing your order.'}
    return results


def create_order(request, order_total, transaction_id):
    order = Order()
    checkout_form = CheckoutForm(request.POST, instance=order)
    order = checkout_form.save(commit=False)
    order.transaction_id = transaction_id
    order.ip_address = request.META.get('REMOTE_ADDR')
    order.status = Order.SUBMITTED
    order.user = None
    order.order_total = order_total
    order_total.purchased = True
    order_total.save()
    if request.user.is_authenticated():
        order.user = request.user
        from accounts import profile

        user_profile = profile.get_profile(request)
        # verificar si campos requeridos estan vacios, si lo estan crear un user_profile para este usuario desde
        # aqui, asi no tendria q escribirlo en el form UserProfileForm
        if not user_profile.email or not user_profile.shipping_name or user_profile.shipping_city == 0:
            profile.set_profile(request)
    order.save()
    # if the order save succeeded
    if order.pk:
        # verificar si el usuario tuvo la promo4, para eliminarla
        try:
            promo4_id = request.session['promo4_id']
            del request.session['promo4_id']
            promo4 = Promo4.objects.get(id=promo4_id)
            promo4.active = False
            promo4.save()
        except KeyError:
            pass
        try:  # eliminar el codigo de promoion para el usuario
            promo_id = request.session['promo3_id']
            del request.session['promo3_id']
            Promo3.objects.get(id=promo_id).delete()
        except KeyError:
            pass
        cart_items = cart.get_cart_items(request)
        for ci in cart_items:
            # create order item for each cart item
            oi = OrderItem()
            oi.order = order
            oi.quantity = ci.quantity
            oi.price = ci.price()  # now using @property
            oi.product = ci.product
            # disminuir del almacen la cant disponible para este prod
            ci.product.quantity -= ci.quantity
            ci.product.save()
            oi.save()
            # all set, empty cart
        cart.empty_cart(request)
    # return the new order object
    return order
