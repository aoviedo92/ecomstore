from django import template
import locale

register = template.Library()


@register.filter(name='currency')
def currency(value, request=None):
    """
    a este filter le traemos la peticion, pq ahi almacenamos la session con los datos de la actual
    moneda a mostrar (cuc, mn)
    """
    if request:
        currency_session = request.session.get("currency_session", {})
    try:
        currency_ = currency_session.get("currency", "cuc")
    except UnboundLocalError:
        currency_ = "cuc"
    if currency_ == "mn":
        value *= 25
        return "$%d.00" % value
    return "$%.2f" % value
