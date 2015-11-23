# coding=utf-8
from random import randint
from django import template
# import tagging
from tagging.models import Tag
from tagging.utils import LOGARITHMIC
from cart import cart
from catalog import forms
from catalog.models import Category, CategoryGroup, CommonCategory, Product
from utils import promo2

register = template.Library()


@register.inclusion_tag("tags/cart_items.html")
def cart_items(request):
    cart_items_ = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)
    return {'cart_items_': cart_items_, 'request': request, 'cart_subtotal': cart_subtotal}


@register.inclusion_tag("tags/cart_num_items.html")
def cart_num_items(request):
    cart_item_count = cart.cart_distinct_item_count(request)
    return {'cart_item_count': cart_item_count}


@register.inclusion_tag("tags/category_list.html")
def category_list(request_path):
    active_categories = Category.active.all()
    active_categories_not_common = active_categories.filter(common=None)
    common = CommonCategory.objects.all()
    return {
        'group_categories': CategoryGroup.objects.all(),
        'active_categories': active_categories,
        'common': common,
        'active_categories_not_common': active_categories_not_common,
        'request_path': request_path
    }


@register.inclusion_tag('tags/category_list_to_layout.html')
def category_list_to_layout(request_path):
    return category_list(request_path)


# @register.inclusion_tag("tags/product_list_.html")
# def product_list(products, header_text):
#     return {'products': products,
#             'header_text': header_text}


@register.inclusion_tag("tags/currency_.html")
def currency_tag(request):
    post = request.session.get("currency_session", {})
    form = forms.Currency(post)
    request_path = request.path
    return {'form': form, 'request_path': request_path}


@register.inclusion_tag("tags/row_products_3_by_3.html")
def group_products(product_row):
    return {"product_list": product_row}


@register.inclusion_tag("catalog/tags_cloud.html")
def tag_cloud():
    product_tags = Tag.objects.cloud_for_model(Product, steps=9,
                                               distribution=LOGARITHMIC,
                                               filters={'is_active': True})
    return locals()


@register.inclusion_tag("catalog/promotions.html")
def tag_promotions():
    promo2_label = []
    category, product = promo2()
    if category and product:
        product_link = u"<a href='%s'>%s</a>" % (product.get_absolute_url(), product)
        category_link = u"<a href='%s'>%s</a>" % (category.get_absolute_url(), category)
        promo2_label = [u"Llévate gratis este producto: %s, si compras dos productos de esta categoría: %s" % (
            product_link, category_link)]
    labels = [u"Si compras +5 artículos obtienes un descuento del 10%",
              u"Participa en nuestras <a href='/rifas/'>rifas</a>...<br/>puedes ser un ganador!",
              u"Conviértete en usuario leal, y podrás beneficiarte en la mayoría de juegos del azar.",
              u"Envío gratis para compras de más de 75cuc",
              u"Si eres usuario leal puedes obtener 5% de descuento de tus compras... Siempre!",
              ]
    if promo2_label:
        labels += promo2_label
    promotion = labels[randint(0, len(labels) - 1)]
    return {'promotion': promotion}
