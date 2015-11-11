from django import template
from django.core.paginator import EmptyPage
from search.forms import SearchForm
import urllib
from slugify import slugify

register = template.Library()


@register.inclusion_tag("tags/search_box.html")
def search_box(request):
    q = request.GET.get('q', '')
    form = SearchForm({'q': q})
    return {'form': form}


@register.inclusion_tag('tags/pagination_links.html')
def pagination_links(request, paginator):
    raw_params = request.GET.copy()
    page = raw_params.get('page', 1)
    pag = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    # construir los parametros get con esta estructura: q=<clave-de-busqueda>&page=<num-de-pag>
    # se puede hacer con urllib.urlencode(raw_params) pero esta forma no tiene en cuenta las cadenas unicode
    # por lo que lanzarian un error UnicodeDecodeError si en la consulta se entro una cadena por ej con tilde.
    params = u""
    for key, value in raw_params.iteritems():
        params += u"%s=%s&" % (key, value)
    num_pages = paginator.num_pages
    return {'request': request,
            'num_pages': num_pages,
            'pag': pag,
            'params': params}
