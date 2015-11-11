from django import template
# import tagging
from tagging.models import Tag
from tagging.utils import LOGARITHMIC
from cart import cart
from catalog import forms
from catalog.models import Category, CategoryGroup, CommonCategory, Product

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