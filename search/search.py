from models import SearchTerm
from catalog.models import Product
from django.db.models import Q, QuerySet
from stats import stats

STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not',
               'of', 'on', 'or', 'that', 'the', 'to', 'with']


def store(request, q, matching):
    """ stores the search text """
    # if search term is at least three chars long, store in db
    if len(q) > 1:
        term = SearchTerm()
        term.q = q
        term.ip_address = request.META.get('REMOTE_ADDR')
        term.tracking_id = stats.__tracking_id(request)
        term.user = None
        if request.user.is_authenticated():
            term.user = request.user
        # salvamos para que no nos salga el error: <SearchTerm: inst> need to have a value for field "searchterm"
        # before this many-to-many relationship can be used.
        term.save()
        for match in matching:
            term.found_products.add(match)


def products(search_text):
    """
    get products matching the search text
    """
    # search_perfomed_before = SearchTerm.objects.filter(q=search_text).order_by('-search_date')
    # if search_perfomed_before:
    #     found_products = search_perfomed_before[0].found_products.all()
    #     return found_products
    words = _prepare_words(search_text)
    prod = Product.active.all()
    results = set()
    for word in words:
        product = prod.filter(Q(name__icontains=word) |
                              Q(description__icontains=word) |
                              Q(sku__iexact=word) |
                              Q(brand__icontains=word) |
                              Q(meta_description__icontains=word) |
                              Q(meta_keywords__icontains=word))
        results = results.union(product)  # efectuar la operacion union de conjuntos
    results = list(results)  # convertir un set() en list() para iterar
    ids = [res.id for res in results]  # sacar cada id de la list de results
    results = prod.filter(id__in=ids)  # crear un queryset()
    return [] if results is None else results


def _prepare_words(search_text):
    """
    strip out common words, limit to 5 words
    """
    words = search_text.split()
    for common in STRIP_WORDS:
        if common in words:
            words.remove(common)
    return words[0:5]

# def _levenshtein(str1, str2):
#     d = dict()
#     for i in range(len(str1) + 1):
#         d[i] = dict()
#         d[i][0] = i
#     for i in range(len(str2) + 1):
#         d[0][i] = i
#     for i in range(1, len(str1) + 1):
#         for j in range(1, len(str2) + 1):
#             d[i][j] = min(d[i][j - 1] + 1, d[i - 1][j] + 1, d[i - 1][j - 1] + (not str1[i - 1] == str2[j - 1]))
#     return d[len(str1)][len(str2)]
