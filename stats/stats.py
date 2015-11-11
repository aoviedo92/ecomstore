import os
import base64
from random import randint
from django.db.models import Count, Avg
from catalog.models import Product
from checkout.models import Order, OrderItem
from ecomstore import settings
from search.models import SearchTerm
from models import ProductView
from utils import take_three_pos

PRODUCTS_PER_ROW = settings.PRODUCTS_PER_ROW


def __tracking_id(request):
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
    return request.session['tracking_id']


def __sort_words_by_frequency(search_string):
    # convert the string to a python list
    words = search_string.split()
    # assign a rank to each word based on frequency
    ranked_words = [[word, words.count(word)] for word in set(words)]
    # sort the words based on descending frequency
    sorted_words = sorted(ranked_words, key=lambda word_: -word_[1])
    # return the list of words, most frequent first
    return [p[0] for p in sorted_words]


def __frequent_search_words(request=None):
    print('stats.py - frequent_search_words')
    # get the ten most recent searches from the database.
    if request:
        users_have_searched = SearchTerm.objects.filter(tracking_id=__tracking_id(request))
        take_field_q = users_have_searched.values('q')
        searches = take_field_q.order_by('-search_date')[0:10]
    else:
        searches = SearchTerm.objects.all().values('q').order_by('-search_date')[0:10]
    # join all of the searches together into a single string.
    search_string = ' '.join([search['q'] for search in searches])
    # return the top three most common words in the searches
    return __sort_words_by_frequency(search_string)[0:3]


def recommended_from_search(request=None):
    print('stats.py - recommended_from_search 1')
    # get the common words from the stored searches
    common_words = __frequent_search_words(request)
    from search.models import SearchTerm

    recommended = set()
    for word in common_words:
        search_terms = SearchTerm.objects.filter(q__icontains=word)
        for term in search_terms:
            if len(recommended) == PRODUCTS_PER_ROW:
                break
            products = term.found_products.all()
            recommended = recommended.union(products)
    # print('rec',recommended)
    return recommended


def log_product_view(request, product):
    """
    cuando un user entra a un producto, se guarda en la db q el user vio ese producto.
    se intenta acceder a un ProductView con este id(tracking_id es un id de la session del usuario, para identificarlo
    aunque no este logueado) y el producto pasado. si no se encuentra este registro, pues se registra.
    """
    t_id = __tracking_id(request)
    try:
        v = ProductView.objects.get(tracking_id=t_id, product=product)
        v.save()
    except ProductView.DoesNotExist:
        v = ProductView()
        v.product = product
        v.ip_address = request.META.get('REMOTE_ADDR')
        v.tracking_id = t_id
        user = request.user if request.user.is_authenticated() else None
        v.user = user
        v.save()


def __get_recently_viewed(request):
    t_id = __tracking_id(request)
    views = ProductView.objects.filter(tracking_id=t_id).values('product_id').order_by('-date')[0:PRODUCTS_PER_ROW]
    product_ids = [v['product_id'] for v in views]
    return Product.active.filter(id__in=product_ids)


def recommended_from_views(request):
    print('stats.py - recommended_from_views 1')
    recommended = []
    # productos recientemente vistos por el usuario. (usamos tracking_id para manejar el la session)
    viewed = __get_recently_viewed(request)
    # si hay productos previamente vistos, obtener otros tracking_ids que hayan visto estos productos tb.
    if viewed:
        product_views = ProductView.objects.filter(product__in=viewed).values('tracking_id')
        # --> [{'tracking_id': t_id1}, {'tracking_id': t_id2}...]
        t_ids = [v['tracking_id'] for v in product_views]
        # if there are other tracking ids, get other products.
        if t_ids:
            all_viewed = Product.active.filter(productview__tracking_id__in=t_ids)
            # if there are other products, get them, excluding the
            # products that the customer has already viewed.
            if all_viewed:
                other_viewed = ProductView.objects.filter(product__in=all_viewed).exclude(product__in=viewed)
                if other_viewed:
                    recommended = Product.active.filter(productview__in=other_viewed).distinct()[:3]
    return recommended if len(recommended) >= 3 else []


def inspired_by_user_shopping_trends(request):
    """
    inspirado por las compras previas del usuario, de las compras del usuario, sacar cada item, de esos item,
    ver a que categoria pertenece, ver cuales son las cat mas presentes, ordenarlas y de esas rankeadas sacar
    los productos recomm
    """
    print('inspired_by_user_shopping_trends')
    user = request.user
    user_orders = Order.objects.filter(user=user)
    # --> [<Order: Order #1>, <Order: Order #2>]
    order_items = OrderItem.objects.filter(order=user_orders)
    # --> [<OrderItem: prod1 (sku)>, <OrderItem: amarillo (sku)>]
    l = []
    sold_products_ids = []  # estos prod los debemos excluir pq ya el usuario los compro
    for o_i in order_items:
        p = o_i.product
        sold_products_ids.append(p.id)
        c = p.categories.all()
        l += [cat for cat in c]
        # --> [<Category: categ1>, <Category: categ1>, <Category: categ2>, <Category: categ2>, <Category: categ2>]
    # ver cual categoria se repite mas, y ordenarlas
    ranked_cat = [[cat, l.count(cat)] for cat in set(l)]
    # --> [[<Category: categ1>, 2], [<Category: categ2>, 3]]
    sorted_cat = sorted(ranked_cat, key=lambda ct: -ct[1])
    # --> [[<Category: categ2>, 3], [<Category: categ1>, 2]]
    try:
        category_1 = sorted_cat[0][0]
        recommended = category_1.product_set.exclude(id__in=sold_products_ids).distinct()[:3]
        # verificar q la dif entre cant de cat de las dos primeras pos no sean muy dispares(menos del doble)
        # esto si hay mas de un resultado
        if len(sorted_cat) >= 2:
            recommended = list(recommended)
            cant1 = sorted_cat[0][1]
            cant2 = sorted_cat[1][1]
            dif = cant2 * 100 / cant1  # part/tot=%/100
            # si la dif cumple, devolver 2 prod de la primera cat, y 1 prod de la segunda cat
            if dif > 50:
                category_2 = sorted_cat[1][0]
                products = category_2.product_set.exclude(id__in=sold_products_ids).distinct()[:3]
                try:
                    recommended[2] = products[0]
                except IndexError:  # si recommended no tiene len(3)
                    for i in range(3 - len(recommended)):  # recorremos desde 0 hasta lo q le falta para llegar a 3
                        recommended.append(products[i])  # cubrimos ese hueco con los prod de esta cat
    except IndexError:  # si no hay ni una categoria en la q buscar
        return []
    return recommended if len(recommended) == 3 else []


class Get3Product:
    def __init__(self, products=None, num_recommend=3):
        self.__products = products if products else Product.active.all()
        self.__num_recommend = num_recommend
        self.__random_labels = [u"Productos nuevos",
                                u"Otros usuarios tambien han buscado",
                                u"Los mas polemicos",
                                u"Deseados",
                                u"Lujosos",
                                u"Rebajas",
                                u"los mas votados",
                                u"grandes rebajas",
                                ]
        self.__function_dict = {
            self.__random_labels[0]: self.__get_3_new,
            self.__random_labels[1]: recommended_from_search,
            self.__random_labels[2]: self.__get_3_polemical,
            self.__random_labels[3]: self.__get_3_desired,
            self.__random_labels[4]: self.__get_3_bestseller,
            self.__random_labels[5]: self.__get_3_sales,
            self.__random_labels[6]: self.__get_3_voted,
            self.__random_labels[7]: self.__get_3_great_sales,
        }

    def __get_3_great_sales(self):
        sales = [product for product in self.__products if product.great_sales()]
        try:
            rand_list = take_three_pos(len(sales) - 1)
            return [sales[rand_list[0]], sales[rand_list[1]], sales[rand_list[2]]]
        except ValueError:
            return []

    def __get_3_voted(self):
        # tomamos para cada producto, su rating promedio, filtramos aquellos cuyo prom sea mas q 3, lo ordenamos
        voted = self.__products.annotate(avg=Avg('productrating__rating')).filter(avg__gt=3).order_by('-avg')
        # reordenamos segun el criterio de q los q tienen mayor cantidad de votos deben ir primero, aunq esto implique
        # q un prod con menos prom quede mas arriba.
        voted = voted.annotate(cant=Count('productrating')).order_by('-cant')
        return voted[:3] if len(voted) >= 3 else None

    def __get_3_sales(self):
        """
        obtener 3 productos al azar que esten en rebajas
        """
        # rebajas por debajo del 45%
        sales = [product for product in self.__products if product.sale_price() and not product.great_sales()]
        try:
            rand_list = take_three_pos(len(sales) - 1)
            return [sales[rand_list[0]], sales[rand_list[1]], sales[rand_list[2]]]
        except ValueError:
            return []

    def __get_3_new(self):
        # print('stats.py - get_3_new')
        new = [product for product in self.__products if product.new_product()]
        if len(new) >= 3:
            rand_list = take_three_pos(len(new) - 1)
            return [new[rand_list[0]], new[rand_list[1]], new[rand_list[2]]]
        return None

    def __get_3_bestseller(self):
        # print('stats.py - get_3_bestseller')
        bestsellers = self.__products.filter(is_bestseller=True)
        if len(bestsellers) >= 3:
            rand_list = take_three_pos(len(bestsellers) - 1)
            return [bestsellers[rand_list[0]], bestsellers[rand_list[1]], bestsellers[rand_list[2]]]
        return None

    def __get_3_polemical(self):
        # print('stats.py - get_3_polemical')
        polemics = self.__products.annotate(num_rev=Count('productreview')).filter(num_rev__gt=2).order_by('-num_rev')
        return polemics[:3] if len(polemics) >= 3 else None

    def __get_3_desired(self):
        # print('stats.py - get_3_desired')
        desired = self.__products.annotate(num_desired=Count('userprofile__wish_list')).filter(
            num_desired__gt=2).order_by('-num_desired')
        return desired[:3] if len(desired) >= 3 else None

    def recommended(self):
        # pos = take_three_pos(len(self.__random_labels) - 1)
        pos = [5, 7, 2]
        print('stats.py - pos', pos)
        recommended_1 = {self.__random_labels[pos[0]]: self.__function_dict[self.__random_labels[pos[0]]]()}
        recommended_2 = {self.__random_labels[pos[1]]: self.__function_dict[self.__random_labels[pos[1]]]()}
        if self.__num_recommend == 2:
            return recommended_1, recommended_2, None
        recommended_3 = {self.__random_labels[pos[2]]: self.__function_dict[self.__random_labels[pos[2]]]()}
        return recommended_1, recommended_2, recommended_3


class RecommendedForUsers:
    def __init__(self, request):
        self.__request = request
        self.__random_labels = [u"Has buscado con frecuencia",
                                u"Has visitado lo que otros han visitado con frecuencia",
                                u"Inspirado por tus tendencias de compra",
                                ]
        self.__function_dict = {
            self.__random_labels[0]: self.__get_recommended_from_search,
            self.__random_labels[1]: self.__get_recommended_from_views,
            self.__random_labels[2]: self.__get_inspired_by_user_shopping_trends,
        }

    def __get_recommended_from_search(self):
        return recommended_from_search(self.__request)

    def __get_recommended_from_views(self):
        return recommended_from_views(self.__request)

    def __get_inspired_by_user_shopping_trends(self):
        return inspired_by_user_shopping_trends(self.__request)

    def recommended(self):
        pos = randint(0, len(self.__random_labels) - 1)
        return {self.__random_labels[pos]: self.__function_dict[self.__random_labels[pos]]()}
