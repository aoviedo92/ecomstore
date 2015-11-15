from django.contrib.auth.models import User
from django.db import models
from catalog.models import Product
from checkout.models import BaseOrderInfo, Order
from manager.models import Promo3

class UserProfile(BaseOrderInfo):
    user = models.OneToOneField(User)
    sex = models.IntegerField(choices=((0, "Seleccione Sexo"), (1, "Femenino"), (2, "Masculino")), max_length=15,
                              default=0)
    # birth_day = models.DateField(null=True)
    wish_list = models.ManyToManyField(Product, blank=True)
    loyal_user = models.BooleanField(blank=True, default=False)
    promo3 = models.OneToOneField(Promo3, null=True, blank=True)

    def __unicode__(self):
        return 'User Profile for: ' + self.user.username

    def is_loyal_user(self):
        count = Order.objects.filter(user=self.user).count()
        if count >= 5:
            self.loyal_user = True
            is_loyal = True
        else:
            self.loyal_user = False
            is_loyal = False
        self.save()
        return is_loyal
