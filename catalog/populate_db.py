from models import *


def create_category(group, i):
    Category.objects.create(name="categ" + str(i), group=group)


def populate_categories():
    i = 0
    category_group = CategoryGroup.objects.all()
    for group in category_group:
        create_category(group, i)
        i += 1
        create_category(group, i)
        i += 1


# def populate_category_groups():
#     CategoryGroup.objects.create(sex=None, name='bufandas')
#     CategoryGroup.objects.create(sex=None, name='invierno')
#     CategoryGroup.objects.create(sex=1, name='blusas')
#     CategoryGroup.objects.create(sex=1, name='bolsos')
#     CategoryGroup.objects.create(sex=2, name='billeteras')
#     CategoryGroup.objects.create(sex=2, name='camisas')


def populate_group_categories():
    for name in ["mujeres", "hombres", "bodas", "tejidos"]:
        CategoryGroup.objects.create(group_name=name)
