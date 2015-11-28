# coding=utf-8
from profile import Profile
from random import shuffle
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core import urlresolvers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg, Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import render_to_string
from tagging.models import Tag, TaggedItem
from accounts import profile
from accounts.models import UserProfile
from cart import cart
from catalog import product_list
from catalog.forms import ProductAddToCartForm, OrderByForm, ProductsPerPageForm, ProductReviewForm, ProductRatingForm
from catalog.models import Category, Product, CategoryGroup, CommonCategory, ProductReview, ProductRating
from django.template import RequestContext
from catalog.product_list import *
from ecomstore import settings
from manager.models import Promo4
from stats import stats
from forms import Currency
import json
from utils import get_product_row
import datetime
import utils
from django.core.cache import cache


def index(request):
    page_title = 'Street Fashion'
    recommendations_for_user_active = True
    if request.user.is_authenticated():
        recommendations_for_user = recommendations_for_user_login(request)
        if len(recommendations_for_user.values()[0]) < 3:
            # try again
            recommendations_for_user = recommendations_for_user_login(request)
            if len(recommendations_for_user.values()[0]) < 3:
                recommendations_for_user_active = False
    recommended_1, recommended_2, recommended_3 = random_recommendations()  # --> {u'Deseados': [<Product: prod14>, <Product: pro11>, <Product: prod12>]}

    all_products = Product.active.all()
    print('all_products',all_products)
    # buscar hasta q encontremos productos que hayan sido comprado juntos
    products_bought_together_key = 'products_bought_together_key'
    products_bought_together = cache.get(products_bought_together_key)
    if not products_bought_together:
        random_list = []
        while True:
            pos = randint(0, len(all_products) - 1)
            if pos not in random_list:
                random_list.append(pos)
                take_random_product = all_products[pos]
                products_bought_together = utils.products_bought_together(take_random_product)
                if products_bought_together:
                    cache.set(products_bought_together_key, products_bought_together, settings.CACHE_TIMEOUT)
                    break
                else:
                    continue
            else:
                continue
    featured_list = all_products.filter(is_featured=True)
    featured_list = list(featured_list)  # transf QuerySet en lista para regar los elems con shuffle
    shuffle(featured_list)
    featured1 = featured_list[:3]
    featured2 = featured_list[3:6]
    return render_to_response("home.html", locals(), context_instance=RequestContext(request))


def show_category(request, category_slug=None, common_name=None):
    # esta vista maneja dos urls q tienen el mismo proposito: mostrar productos agrupados por categorias.
    if category_slug:
        # para una categoria en especifico
        category_cache_key = request.path
        c = cache.get(category_cache_key)
        if not c:
            print('cat not in cache')
            c = get_object_or_404(Category, slug=category_slug)
            cache.set(category_cache_key, c, settings.CACHE_TIMEOUT)
        products = c.product_set.filter(is_active=True)
        title_head = c.name
        page_title = title_head
    elif common_name:
        # para una categoria q es comun a otras categorias (almacena categorias)
        # como Accesorios, es comun a Accesorios de bodas, Accesorios de mujeres, Accesorios tejidos...
        common_category_cache_key = request.path
        common = cache.get(common_category_cache_key)
        if not common:
            print('cat common not in cache')
            common = get_object_or_404(CommonCategory, common_name=common_name)
            cache.set(common_category_cache_key, common, settings.CACHE_TIMEOUT)
        common_categories = common.category_set.all()
        title_head = common.common_name
        page_title = title_head
        products = Product.active.filter(categories__in=common_categories).distinct()
    else:
        title_head = "Productos"
        page_title = title_head
        products = Product.active.all()[0:20]
    # random_products = products
    recommended_1, recommended_2, recommended_3 = random_recommendations(products, 2)

    products, order_by_form = order_products(request, products)
    num_x_pag, product_per_pag_form = get_num_x_pag(request)
    products, order_by_brand_form = filter_products(request, products)
    paginator, products_per_pag = get_paginator(request, products, num_x_pag)
    product_row = get_product_row(products_per_pag)
    show_toolbar = True
    return render_to_response("tags/product_list.html", locals(), context_instance=RequestContext(request))


def tag(request, tag_):
    title_head = "Etiquetado con " + tag_
    page_title = title_head
    products = TaggedItem.objects.get_by_model(Product.active, tag_)

    products, order_by_form = order_products(request, products)
    num_x_pag, product_per_pag_form = get_num_x_pag(request)
    products, order_by_brand_form = filter_products(request, products)
    paginator, products_per_pag = get_paginator(request, products, num_x_pag)
    product_row = get_product_row(products_per_pag)

    return render_to_response("tags/product_list.html", locals(), context_instance=RequestContext(request))


def quick_access(request, quick_access_slug):
    quick_access_ = stats.QuickAccess()
    switch_dict = {'new_products': quick_access_.new_products,
                   'discounts': quick_access_.discount,
                   'top_sellers': quick_access_.top_sellers,
                   'polemical': quick_access_.polemical,
                   'top_searches': quick_access_.top_searches,
                   'desired': quick_access_.desired,
                   'bestseller': quick_access_.bestseller,
                   'voted': quick_access_.voted,
                   'featured': quick_access_.featured,
                   'super_discount': quick_access_.super_discount
                   }
    products = switch_dict[quick_access_slug]()
    product_row = get_product_row(products)
    product_row.reverse()
    page_title = quick_access_slug
    return render_to_response("tags/product_list_quick_access.html", locals(), context_instance=RequestContext(request))


def show_product(request, product_slug):
    """
    new product view, with POST vs GET detection
    """
    p = get_object_or_404(Product, slug=product_slug)
    page_title = p.name
    meta_keywords = p.meta_keywords
    meta_description = p.meta_description
    if request.method == 'POST':
        # add to cart... create the bound form
        post_data = request.POST.copy()
        product_add_to_cart_form = ProductAddToCartForm(request, post_data)
        # check if posted data is valid
        if product_add_to_cart_form.is_valid():
            # add to cart and redirect to cart page
            cart.add_to_cart(request)
            # if test cookie worked, get rid of it
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                # url = urlresolvers.reverse('show_cart')
                # return HttpResponseRedirect(url)
    else:
        # it's a GET, create the unbound form. Note request as a kwarg
        product_add_to_cart_form = ProductAddToCartForm(request=request, label_suffix=':')
        # assign the hidden input the product slug
        product_add_to_cart_form.fields['product_slug'].widget.attrs['value'] = product_slug
        # set the test cookie on our first GET request
        request.session.set_test_cookie()
    stats.log_product_view(request, p)

    customers_who_bought_this_p_also_bought = utils.products_bought_together(p)

    product_reviews = ProductReview.approved.filter(product=p).order_by('-date')
    review_form = ProductReviewForm()
    review_rating = ProductRatingForm()
    # rating promedio
    avg_rating = p.avg_rating()
    cant_rating = p.productrating_set.count()
    desired_by_user = False
    user_already_voted = 0
    if request.user.is_authenticated():
        # el usuario loguead ya voto por este prod?
        try:
            user_product_rating = ProductRating.objects.get(user=request.user, product=p)
            user_already_voted = user_product_rating.rating
        except ProductRating.DoesNotExist:
            user_already_voted = 0
        # deseado por el usuario logueado?
        user_profile = profile.get_profile(request)
        if p in user_profile.wish_list.all():
            desired_by_user = True
    return render_to_response("catalog/product.html", locals(), context_instance=RequestContext(request))


def currency(request):
    url = '/'
    if request.method == 'POST':
        url = request.POST.get("current_url")
        request.session["currency_session"] = request.POST
    return HttpResponseRedirect(url)


@login_required
def add_review(request):
    """
    AJAX view that takes a form POST from a user submitting a new product review;
    requires a valid product slug and args from an instance of ProductReviewForm;
    return a JSON response containing two variables: 'review', which contains
    the rendered template of the product review to update the product page,
    and 'success', a True/False value indicating if the save was successful.
    """
    slug = request.POST.get('slug')
    product = Product.active.get(slug=slug)

    # errors = True
    content = request.POST.get('content')
    template = "catalog/product_review.html"
    if content.strip() != "":
        review = ProductReview.objects.create(
            product=product,
            user=request.user,
            content=content
        )
        review.save()
        html = render_to_string(template, {'review': review})
        response = json.dumps({'success': 'True', 'html': html})
    else:
        response = json.dumps({'success': 'False', 'html': ""})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@login_required
def add_vote(request):
    # si un user ya voto, y vuelve a votar, actualizar su voto por el nuevo
    rating = request.POST.get('rating')
    slug = request.POST.get('slug')
    product = Product.active.get(slug=slug)
    try:
        user_product_rating = ProductRating.objects.get(user=request.user, product=product)
        old_rating = user_product_rating.rating
        print(old_rating)
        user_product_rating.rating = rating
        user_product_rating.save()
        print(rating, user_product_rating.rating)
        comment_about_user_voted = u"Lástima que hayas desvalorado este producto, déjanos saber por qué en los comentarios" \
            if int(old_rating) > int(rating) else u"Excelente! opina en los comentarios"

    except ProductRating.DoesNotExist:
        ProductRating.objects.create(
            rating=rating,
            user=request.user,
            product=product
        )
        comment_about_user_voted = u"Gracias por tu voto favorable, déjanos tu opinión en los comentarios!" \
            if int(
            rating) > 3 else u"Sentimos que no te agrade tanto este producto, déjanos tu opinión en los comentarios"
    avg_rating = product.avg_rating()
    response = json.dumps(
        {'avg_rating': avg_rating, 'rating': rating, 'comment_about_user_voted': comment_about_user_voted})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@login_required
def add_wish_list(request):
    slug = request.POST.get('slug')
    product = Product.active.get(slug=slug)
    print("product", product)
    user_profile = profile.get_profile(request)
    print("wishlist", user_profile.wish_list.all())
    if product not in user_profile.wish_list.all():
        user_profile.wish_list.add(product)
        response = json.dumps({'success': 'True'})
    else:
        response = json.dumps({'success': 'False'})
    print("wishlist", user_profile.wish_list.all())
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@login_required
def remove_wish_list(request):
    slug = request.POST.get('slug')
    product = Product()
    user_profile = profile.get_profile(request)
    try:
        product = user_profile.wish_list.get(slug=slug)
        user_profile.wish_list.remove(product)
        response = json.dumps({'success': 'True'})
    except product.DoesNotExist:
        response = json.dumps({'success': 'False'})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@login_required
def add_tag(request):
    tags = request.POST.get('tag', '')
    slug = request.POST.get('slug', '')
    if len(tags) > 2:
        p = Product.active.get(slug=slug)
        html = u''
        template = "catalog/tag_link.html"
        for tag in tags.split():
            tag.strip(',')
            Tag.objects.add_tag(p, tag)
        for tag in p.tags:
            html += render_to_string(template, {'tag': tag})
        response = json.dumps({'success': 'True', 'html': html})
    else:
        response = json.dumps({'success': 'False'})
    return HttpResponse(response, content_type='application/javascript; charset=utf8')


def rifas(request):
    promo4 = Promo4.objects.filter(active=True)
    promo4 = [promo for promo in promo4 if promo.is_open]
    user_include = False
    for promo in promo4:
        if request.user in promo.users.all():
            user_include = True
            user_in_rifa = promo.id
            break
    page_title = 'rifas'
    return render_to_response("catalog/rifas.html", locals(), context_instance=RequestContext(request))
