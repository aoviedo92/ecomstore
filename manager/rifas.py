# -*- coding: utf-8 -*-
import json
from random import randint
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from manager.models import Promo4


def test_superuser(user):
    return user.is_superuser


@login_required
def add_user_rifas(request):
    """
    ajax para apuntarse a una rifa
    """
    users_iscritos = 0
    if request.POST:
        promo_id = request.POST.get('promo_id')
        promo = Promo4.objects.get(id=promo_id)
        users_iscritos = promo.users.count()
        if request.user not in promo.users.all():
            promo.users.add(request.user)
            promo.save()
            users_iscritos = promo.users.count()

    response = json.dumps({'success': 'true', 'users_inscritos': users_iscritos})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@login_required
def remove_user_rifas(request):
    """
    funcion llamada por ajax, para darse de baja de la rifa
    """
    users_inscritos = 0
    if request.POST:
        promo_id = request.POST.get('promo_id')
        promo = Promo4.objects.get(id=promo_id)
        users_inscritos = promo.users.count()
        if request.user in promo.users.all():
            promo.users.remove(request.user)
            promo.save()
            users_inscritos = promo.users.count()

    response = json.dumps({'success': 'true', 'users_inscritos': users_inscritos})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


def retrieve_info(request):
    """
    al pararse arriba de una rifa se ejecuta por ajax esta view, que brinda info acerca de la rifa
    """
    promo_id = request.POST.get('promoid')
    promo = Promo4.objects.get(id=promo_id)
    total = promo.products.aggregate(Sum('price'))['price__sum']
    percent = promo.discount
    discount = total * percent / 100
    total_discount = total - discount
    data = u"Con un total de $%.2f y un descuento del %d%%<br/>llévate estos productos sólo por: $%s" % (
        total, percent, total_discount)
    response = json.dumps({"data": data})

    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@user_passes_test(test_superuser)
def rifas_results(request):
    """
    mostrar las rifas cerradas, pero no las no activas
    """
    promos = Promo4.objects.all()
    closed_promos = [promo for promo in promos if not promo.is_open and promo.active]
    return render_to_response('manager/promo4_results.html', locals(), context_instance=RequestContext(request))


@user_passes_test(test_superuser)
def get_winner_user(request):
    """
    LLAMADA ajax cuando cuando seleccionamos una rifa cerrada para obtener un random winner
    """
    promo_id = request.POST.get('selected_rifa_id')
    promo = Promo4.objects.get(id=promo_id)
    users = promo.users.all()
    try:
        winner_user = users[randint(0, len(users) - 1)]
        promo.winner_user = winner_user
        promo.active = False
        promo.save()
        response = json.dumps({'result': 'el usuario ganador fue %s' % unicode(winner_user)})
    except ValueError:
        response = json.dumps({'result': 'No se inscribieron usuarios en esta rifa'})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')
