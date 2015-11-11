from django.contrib.auth.models import User
from django.db import models
from catalog.models import Product
from checkout.models import BaseOrderInfo


class UserProfile(BaseOrderInfo):
    user = models.OneToOneField(User)
    sex = models.IntegerField(choices=((0, "Seleccione Sexo"), (1, "Femenino"), (2, "Masculino")), max_length=15,
                              default=0)
    # birth_day = models.DateField(null=True)
    wish_list = models.ManyToManyField(Product, blank=True)

    def __unicode__(self):
        return 'User Profile for: ' + self.user.username
