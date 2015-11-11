import random
# from cart.models import CartItem
import decimal
from models import CartItem
from catalog.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

CART_ID_SESSION_KEY = 'cart_id'


def _cart_id(request):
    """
    get the current user's cart id, sets new one if blank;
    Note: the syntax below matches the text, but an alternative,
    clearer way of checking for a cart ID would be the following:
    if not CART_ID_SESSION_KEY in request.session:
    """
    if request.session.get(CART_ID_SESSION_KEY, '') == '':
        request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
    return request.session[CART_ID_SESSION_KEY]


def _generate_cart_id():
    """ function for generating random cart ID values """
    cart_id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    cart_id_length = 50
    for y in range(cart_id_length):
        cart_id += characters[random.randint(0, len(characters) - 1)]
    return cart_id


def get_cart_items(request):
    """
    return all items from the current user's cart
    """
    return CartItem.objects.filter(cart_id=_cart_id(request))


def add_to_cart(request, product=None):
    """
    function that takes a POST request and adds a product instance to the current customer's shopping cart
    """
    post_data = request.POST.copy()
    # quantity = post_data.get('quantity', 1)  # get quantity added, return 1 if empty
    quantity = 1
    if not product:
        product_slug = post_data.get('product_slug', '')  # get product slug from post data, return blank if empty
        product = get_object_or_404(Product, slug=product_slug)  # fetch the product or return a missing page error
    cart_products = get_cart_items(request)  # get products in cart
    product_in_cart = False
    # check to see if item is already in cart
    for cart_item in cart_products:
        if cart_item.product.id == product.id:
            cart_item.augment_quantity(quantity)  # update the quantity if found
            product_in_cart = True
            break
    if not product_in_cart:
        ci = CartItem()  # create and save a new cart item
        ci.product = product
        ci.quantity = quantity
        ci.cart_id = _cart_id(request)
        ci.save()

def add_to_cart_list_products(request, product_slug_list):
    for product_slug in product_slug_list:
        product = get_object_or_404(Product, slug=product_slug)
        add_to_cart(request, product)

def cart_distinct_item_count(request):
    """
    returns the total number of items in the user's cart
    """
    return get_cart_items(request).count()


def cart_subtotal(request):
    """
    gets the subtotal for the current shopping cart
    """
    cart_total = decimal.Decimal('0.00')
    cart_products = get_cart_items(request)
    for item in cart_products:
        cart_total += item.product.price * item.quantity
    return cart_total


def get_single_item(request, item_id):
    return get_object_or_404(CartItem, id=item_id, cart_id=_cart_id(request))


def remove_from_cart(request):
    """
    remove a single item from cart
    function that takes a POST request removes a single product instance from the current customer's
    shopping cart
    """
    post_data = request.POST.copy()
    item_id = post_data['item_id']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        cart_item.delete()


def update_cart(request):
    """
    function takes a POST request that updates the quantity for single product instance in the
    current customer's shopping cart
    """
    post_data = request.POST.copy()
    item_id = post_data['item_id']
    quantity = post_data['quantity']
    cart_item = get_single_item(request, item_id)
    if cart_item:
        try:
            if int(quantity) > 0:
                cart_item.quantity = int(quantity)
                cart_item.save()
            else:
                remove_from_cart(request)
        except ValueError:  # por si la entrada en el input Update es una letra
            pass


def is_empty(request):
    return cart_distinct_item_count(request) == 0


def empty_cart(request):
    """ empties the shopping cart of the current customer """
    user_cart = get_cart_items(request)
    user_cart.delete()
