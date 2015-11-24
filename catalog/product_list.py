from random import randint
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models.query import QuerySet
from catalog.forms import OrderByForm, ProductsPerPageForm, OrderByBrandForm
from ecomstore import settings
from search import search
from search.models import SearchTerm
from stats.stats import *


def __get_num_x_pag_session(request):
    """
    devolver valor para la cantidad de prod x paginas.
    esto se almacena en una session. si no existe el valor usamos el valor por defecto del settings.py
    """
    return request.session.get('num_x_pag', settings.PRODUCTS_PER_PAGE)


def __get_selected_brand_session(request):
    return request.session.get('selected_brand', "0")


def order_products(request, products):
    """
    :param request:
    :param products: lista de productos de tipo QuerySet
    :return: productos ordenados, y la instancia del form de ordanamiento
    """
    if not products:
        # todo fix bug: realice una busqueda, le puse ver 18results y mostro busq vacia
        # si no hay productos es pq este metodo es llamado desde search/views.py
        # obtenemos la cadena de busqueda de la session donde se guardo
        # buscamos en la db para esa cadena, q resultados(productos) arrojo.
        # si arroja la excep es pq el usuario entro una cadena de len 1 y eso no lo almacenamos en la db
        # No puede haber ninguna categoria vacia, si esto ocurre, al entrar en una url por ej category/categ3/
        # y categ3 esta vacia (sin productos) entonces entramos a este if, pero no queremos este comportamiento
        # y se lanza un excep KeyError pq no se va a encontrar la cookie de busqueda
        search_key = request.session['search_key']
        try:
            found_products = SearchTerm.objects.filter(q=search_key).order_by('-search_date')[0].found_products.all()
        except IndexError:  # por si found_products es []
            found_products = search.products(search_key)
        products = found_products
    order_dict = {'created_at': 'created_at', 'name': 'name', 'brand': 'brand', 'price': 'price'}
    if request.method == "POST":
        # ordenar
        order_by_form = OrderByForm(request.POST, label_suffix=" ")
        option = request.POST.get('order_by', 'created_at')
        order_by = order_dict[option]
        if 'submit_up.x' in request.POST:
            # si se quiere ordenar ascendente
            order_by = "-" + order_by
        products = products.order_by(order_by)
    else:
        products = products.order_by('created_at')
        order_by_form = OrderByForm(label_suffix=" ")

    return products, order_by_form


def get_num_x_pag(request):
    """
    obtener la cant de product por pag, lo cual auxilia al paginator.
    si la peticion es get debe tener un valor "products_per_page", si no, tomamos el valor guardado en la sesion.
    vinculamos el form "product_per_pag_form" con este dato.
    si se actualiza "num_x_pag" lo guardamos en la sesion(actualizar el que ya esta).
    devolvemos este dato y la instancia del form.
    """
    num_x_pag_session = __get_num_x_pag_session(request)

    if request.method == "GET":
        num_x_pag = request.GET.get("products_per_page", num_x_pag_session)
    else:
        num_x_pag = num_x_pag_session
    product_per_pag_form = ProductsPerPageForm({u'products_per_page': unicode(num_x_pag)})
    request.session['num_x_pag'] = num_x_pag
    return num_x_pag, product_per_pag_form


def filter_products(request, products):
    selected_brand_session = __get_selected_brand_session(request)
    # filtrar por marca
    if request.method == "GET":
        selected_brand = request.GET.get("order_by_brand", selected_brand_session)
        if selected_brand != "0":
            # print('filtrar',selected_brand)
            # print(products)
            products = products.filter(brand=selected_brand)
            # print(products)
    else:
        selected_brand = selected_brand_session
    # filtrar por precio
    if request.method == "POST":
        min_price = request.POST.get("min_price")
        max_price = request.POST.get("max_price")
        if not min_price:
            min_price = "0"
        if not max_price:
            max_price = "100000"
        products = products.filter(price__gt=min_price, price__lt=max_price)

    order_by_brand_form = OrderByBrandForm({u"order_by_brand": unicode(selected_brand)}, label_suffix=" ")
    request.session['selected_brand'] = selected_brand
    print('brand',selected_brand)
    return products, order_by_brand_form


def get_paginator(request, products, num_x_pag):
    """
    crear paginator para la lista de products segun num x pag
    """
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1

    paginator = Paginator(products, num_x_pag)

    try:
        products_per_pag = paginator.page(page).object_list
    except (InvalidPage, EmptyPage):
        products_per_pag = paginator.page(1).object_list

    return paginator, products_per_pag


def random_recommendations(products=None, num_recommend=3):
    get_3_product = Get3Product(products, num_recommend)
    recommended_1, recommended_2, recommended_3 = get_3_product.recommended()
    return recommended_1, recommended_2, recommended_3


def recommendations_for_user_login(request):
    recommendations_for_user = RecommendedForUsers(request)
    return recommendations_for_user.recommended()
