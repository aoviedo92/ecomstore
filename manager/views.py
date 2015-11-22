# coding=utf-8
from decimal import Decimal
import glob
import json
from random import randint
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from accounts.models import UserProfile
from catalog.models import CategoryGroup, CommonCategory, Category, Product
from manager.models import Promo3, Promo4
from utils import generate_random_id


@login_required
def promo3(request):
    if request.POST:
        post_data = request.POST.copy()
        users = post_data.getlist('user', [])
        discount = post_data.get('discount', '10')
        print('disc', discount)
        print(users)
        for user in users:
            user_ = User.objects.get(username=user)
            print('user_', user_)
            # up = UserProfile.objects.get(user=user_)
            # print('up',up)
            code = generate_random_id()
            print('code', code)
            promo = Promo3.objects.create(user=user_, code=code, discount=discount)
            print('promo', promo)
            promo.save()
            # print('promo save',promo)
            # up.promo3 = promo
            # up.save()
            # print('up.promo3',up.promo3)
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
    post_data = request.POST.copy()
    loyal_users = post_data.get('loyal_users')
    # users = User.objects.all()
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


def create_group_categories(request):
    group = ["Hombres", "Mujeres", "Bodas", "Tejidos", "Uniformes"]
    for group_name in group:
        CategoryGroup.objects.create(group_name=group_name)
    commons = ['Accesorios', 'Conjuntos', 'Carteras', 'Blusas', u'Bañadores']
    for common in commons:
        CommonCategory.objects.create(common_name=common)
    Category.objects.create(name='Trajes para hombres', slug='trajes-para-hombres',
                            group=CategoryGroup.objects.get(group_name='Bodas'), sex=2)
    Category.objects.create(name='Trajes para mujeres', slug='trajes-para-mujeres',
                            group=CategoryGroup.objects.get(group_name='Bodas'), sex=1)
    Category.objects.create(name='Abrigos', slug='abrigos', group=CategoryGroup.objects.get(group_name='Hombres'),
                            sex=2)
    Category.objects.create(name='Jeans', slug='jeans', group=CategoryGroup.objects.get(group_name='Hombres'), sex=2)
    Category.objects.create(name='Pulovers', slug='pulovers', group=CategoryGroup.objects.get(group_name='Hombres'),
                            sex=2)
    Category.objects.create(name='Conjuntos para hombres', slug=slugify('Conjuntos para hombres'),
                            common=CommonCategory.objects.get(common_name="Conjuntos"),
                            group=CategoryGroup.objects.get(group_name='Hombres'), sex=2)
    Category.objects.create(name='Conjuntos para mujeres', slug=slugify('Conjuntos para mujeres'),
                            common=CommonCategory.objects.get(common_name="Conjuntos"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Accesorios para mujeres', slug=slugify('Accesorios para mujeres'),
                            common=CommonCategory.objects.get(common_name="Accesorios"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Blusas para mujeres', slug=slugify('Blusas para mujeres'),
                            common=CommonCategory.objects.get(common_name="Blusas"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Carteras para mujeres', slug=slugify('Carteras para mujeres'),
                            common=CommonCategory.objects.get(common_name="Carteras"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name=u'Bañadores para mujeres', slug=slugify(u'Bañadores para mujeres'),
                            common=CommonCategory.objects.get(common_name=u"Bañadores"),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name=u'Gafas', slug=slugify(u'Gafas'),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name=u'Vestidos', slug=slugify(u'Vestidos'),
                            group=CategoryGroup.objects.get(group_name='Mujeres'), sex=1)
    Category.objects.create(name='Accesorios tejidos', slug=slugify('Accesorios tejidos'),
                            common=CommonCategory.objects.get(common_name="Accesorios"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name='Blusas tejidas', slug=slugify('Blusas tejidas'),
                            common=CommonCategory.objects.get(common_name="Blusas"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name='Carteras tejidas', slug=slugify('Carteras tejidas'),
                            common=CommonCategory.objects.get(common_name="Carteras"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name=u'Bañadores tejidos', slug=slugify(u'Bañadores tejidos'),
                            common=CommonCategory.objects.get(common_name=u"Bañadores"),
                            group=CategoryGroup.objects.get(group_name='Tejidos'), sex=1)
    Category.objects.create(name=u'Bebé', slug=slugify(u'Bebé'), group=CategoryGroup.objects.get(group_name='Tejidos'),
                            sex=1)
    Category.objects.create(name='Uniformes para hombres', slug='uniformes-para-hombres',
                            group=CategoryGroup.objects.get(group_name='Uniformes'), sex=2)
    Category.objects.create(name='Uniformes para mujeres', slug='uniformes-para-mujeres',
                            group=CategoryGroup.objects.get(group_name='Uniformes'), sex=1)


def create_products(request):
    category_list = Category.objects.all()
    for category in category_list:
        try:
            create_product_aux(category)
        except:
            pass
    return HttpResponse()


def create_product_aux(category):
    cant = randint(7, 10)
    cent_list = [00, 05, 15, 25, 35, 45, 55, 65, 75, 85, 95]  # la parte de los centavos $xx.95
    for i in range(0, cant):
        name = '%s %d' % (category.name, i)
        image = 'image%d' % i
        doll = randint(10, 50)
        cent = cent_list[randint(0, len(cent_list) - 1)]
        price = Decimal('%d.%d' % (doll, cent))
        product = Product.objects.create(name=name, slug=slugify(name), image=image, price=price)
        product.categories.add(category)
        product.save()


def send_mail(request):
    from django.core.mail import send_mail

    send_mail('Subject here', 'Here is the message.', 'aoviedo@estudiantes.uci.cu',
              ['aoviedo@estudiantes.uci.cu'], fail_silently=False)
    return HttpResponse()


def add_user_rifas(request):
    # print(request.POST)
    users_iscritos = 0
    if request.POST:
        promo_id = request.POST.get('promo_id')
        promo = Promo4.objects.get(id=promo_id)
        users_iscritos = promo.users.count()
        if request.user in promo.users.all():
            print('user esta')
        else:
            promo.users.add(request.user)
            promo.save()
            users_iscritos = promo.users.count()

    response = json.dumps({'success': 'true', 'users_inscritos': users_iscritos})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


def remove_user_rifas(request):
    print('remove')
    users_inscritos = 0
    if request.POST:
        promo_id = request.POST.get('promo_id')
        promo = Promo4.objects.get(id=promo_id)
        users_inscritos = promo.users.count()
        if request.user in promo.users.all():
            print('user esta x')
            promo.users.remove(request.user)
            promo.save()
            users_inscritos = promo.users.count()

    response = json.dumps({'success': 'true', 'users_inscritos': users_inscritos})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')


def retrieve_info(request):
    print('retrie')
    print(request.POST.get('promoid'))
    promo_id = request.POST.get('promoid')
    promo = Promo4.objects.get(id=promo_id)
    total = promo.products.aggregate(Sum('price'))['price__sum']
    percent = promo.discount
    discount = total * percent / 100
    data = u"Con un total de $%.2f y un descuento del %d%%<br/>llévate estos productos sólo por: $%s" % (total, percent, discount)
    response = json.dumps({"data": data})

    return HttpResponse(response, content_type='application/javascript; charset=utf-8')
