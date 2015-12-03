# -*- coding: utf-8 -*-
import json
from random import randint
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from accounts.models import UserProfile
from manager.models import Promo3
from utils import generate_random_id

__author__ = 'adrian'


def test_superuser(user):
    return user.is_superuser


@user_passes_test(test_superuser)
def promo3(request):
    """
    asignar codigo de descuento a una lista de usuarios
    """
    if request.POST:
        post_data = request.POST.copy()
        users = post_data.getlist('user', [])
        discount = post_data.get('discount', '10')
        for user in users:
            user_ = User.objects.get(username=user)
            code = generate_random_id()
            promo = Promo3.objects.create(user=user_, code=code, discount=discount)
            promo.save()
    return render_to_response('manager/promo3.html', locals(), context_instance=RequestContext(request))


@user_passes_test(test_superuser)
def promo3_find_users(request):
    """
    buscar usuarios con ajax
    """
    post_data = request.POST.copy()
    find_user = post_data.get('find_user', '')
    template = "manager/include_checkbox.html"
    if find_user:
        # todo excluir de la consulta los usuarios que ya tienen un cupon de descuento
        users = User.objects.filter(username__icontains=find_user)
        html = render_to_string(template, {'users': users})
        response = json.dumps({'html': html})
    else:
        response = json.dumps({'html': ""})

    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@user_passes_test(test_superuser)
def promo3_random_users(request):
    """
    seleccionar usuarios al azar, si esta marcado la casilla para usuarios leales la busqueda se concentra en ellos
    """
    post_data = request.POST.copy()
    loyal_users = post_data.get('loyal_users')
    user_profiles = UserProfile.objects.all()
    if loyal_users == 'true':
        user_profiles = user_profiles.filter(loyal_user=True)
    user_ids = [id['user'] for id in user_profiles.values('user')]
    users = User.objects.filter(id__in=user_ids)
    count = user_profiles.count()
    template = "manager/include_checkbox.html"
    taken_pos = []
    take_users = []
    cant_user_to_take = randint(1, 5)
    if count <= cant_user_to_take:
        cant_user_to_take = count
    for i in range(cant_user_to_take):
        while True:
            pos = randint(0, count - 1)
            if pos not in taken_pos:
                taken_pos.append(pos)
                take_users.append(users[pos])
                break
    html = render_to_string(template, {'users': take_users})
    response = json.dumps({'html': html})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')
