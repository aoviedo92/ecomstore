from random import randint
from ecomstore import settings


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