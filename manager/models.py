from django.db import models
from django.contrib.auth.models import User


class Promo3(models.Model):
    """
    Promocion por codigo de rebaja, le llegan a los usuarios un codigo que podran introducir
    en el carrito de compras, este codigo viene asociado a un % de descuento
    """
    user = models.OneToOneField(User)
    code = models.CharField(max_length=6, unique=True)
    discount = models.IntegerField()

    def __unicode__(self):
        return str(self.user) + "-->" + self.code

