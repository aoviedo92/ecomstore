# coding=utf-8
from random import randint, random
from catalog.models import Product, Promo2
from ecomstore import settings
# import stats.stats


def get_product_row(products_per_pag):
    """
    segun la plantilla usada, una fila de products tiene 3 productos, pero para mantener los css impuestos por esta
    plantilla tengo q en una lista de product, convertirla en una lista con listas de 3 en 3.
    [p1, p2, p3, p4, p5] ---> [[p1, p2, p3], [p4, p5]]
    """
    product_row = []  # lista que almacena filas de prod de 3 en e [[p1,p2,p3],[p4,p5,p6]...]
    row = []
    rest = []  # cuando se quedan prod sin ser add a product_row debido a q no se llega a len(row) == prod_x_row
    products = list(products_per_pag)  # castearlo pq el tipo original es QuerySet el cual no tiene el metodo pop()
    while len(products):
        product = products.pop()
        row.append(product)
        rest.append(product)
        if len(row) == settings.PRODUCTS_PER_ROW:
            product_row.append(row)
            row = []
            rest = []
    product_row.append(rest)
    return product_row


def take_three_pos(length):
    """
    tomar 3 valores aleatorios sin repetir, entre 0 y length
    """
    rand_list = []
    while True:
        new_rand = randint(0, length)
        if new_rand not in rand_list:
            rand_list.append(new_rand)
            if len(rand_list) == 3:
                break
    return rand_list


def products_bought_together(product):
    from stats import stats
    # buscar que productos se han vendido junto con este, mediante la Order lo buscamos
    order = stats.customers_who_bought_this_item_also_bought(product)
    # de esa orden sacar los productos vendidos
    if order:
        ids = order.orderitem_set.all().values('product')  # --> [{'product': 13}, {'product': 14}, {'product': 15}]
        ids = [prod_id['product'] for prod_id in ids]  # --> [13, 14, 15]
        return Product.active.filter(id__in=ids)
    return False


def promotions():
    # calculos para la promo2
    category, product = promo2()
    product_link = "<a href='%s'>%s</a>" % (product.get_absolute_url(), product)
    category_link = "<a href='%s'>%s</a>" % (category.get_absolute_url(), category)

    labels = [u"Si compras +5 artículos obtienes un descuento del 10%",
              u"Llévate gratis este producto: %s, si compras dos productos de esta categoría: %s" % (
              product_link, category_link)]
    pos = 1
    return labels[pos]


def promo2():
    promo = Promo2.objects.first()
    category = promo.category
    product = promo.product
    print('promo',category,product)
    return category, product

def generate_random_id(id_length=6):
    _id = ''
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
    for y in range(id_length):
        _id += characters[randint(0, len(characters) - 1)]
    return _id