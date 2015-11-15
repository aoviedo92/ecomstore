import json
from random import randint
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from accounts.models import UserProfile
from manager.models import Promo3
from utils import generate_random_id


@login_required
def promo3(request):
    if request.POST:
        post_data = request.POST.copy()
        users = post_data.getlist('user', [])
        discount = post_data.get('discount', '10')
        print(users)
        for user in users:
            user_ = User.objects.get(username=user)
            up = UserProfile.objects.get(user=user_)
            code = generate_random_id()
            promo = Promo3.objects.create(code=code, discount=discount)
            promo.save()
            up.promo3 = promo
    return render_to_response('manager/promo3.html', locals(), context_instance=RequestContext(request))


@login_required
def promo3_find_users(request):
    post_data = request.POST.copy()
    find_user = post_data.get('find_user', '')
    template = "manager/include_checkbox.html"
    if find_user:
        users = User.objects.filter(username__icontains=find_user)
        html = render_to_string(template, {'users': users})
        response = json.dumps({'html': html})
    else:
        response = json.dumps({'html': ""})

    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


@login_required
def promo3_random_users(request):
    users = User.objects.all()
    count = users.count()
    template = "manager/include_checkbox.html"
    taken_pos = []
    take_users = []
    cant_user_to_take = randint(1, 5)
    # print(cant_user_to_take)
    for i in range(cant_user_to_take):
        while True:
            pos = randint(2, count - 1)
            if pos not in taken_pos:
                taken_pos.append(pos)
                take_users.append(users[pos])
                break
    html = render_to_string(template, {'users': take_users})
    response = json.dumps({'html': html})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')
