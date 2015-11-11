from django import template

register = template.Library()


@register.inclusion_tag('tags/pagination_products.html')
def pagination_links(request, paginator):
    raw_params = request.GET.copy()
    page = raw_params.get('page', 1)
    pag = paginator.page(page)
    try:
        del raw_params['page']
    except KeyError:
        pass
    params = u""
    for key, value in raw_params.iteritems():
        params += u"%s=%s&" % (key, value)
    num_pages = paginator.num_pages
    return {'request': request,
            'num_pages': num_pages,
            'pag': pag,
            'params': params}
