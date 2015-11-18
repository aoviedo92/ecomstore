from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product, Category
import datetime

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


class Promo4(models.Model):
    """
    rifas gratis, escogemos 3 productos, y q los usuarios se vayan registrando en la rifa
    """
    products = models.ManyToManyField(Product)
    users = models.ManyToManyField(User, null=True, blank=True, related_name='usuarios inscritos')
    winner_user = models.ForeignKey(User, null=True, blank=True, related_name='usuario ganador')
    valid_until = models.DateField()

    def __unicode__(self):
        products = self.products.all()
        chain = ''
        for product in products:
            chain += unicode(product) + '--'
        return chain[:-2]

    @property
    def is_open(self):
        today = datetime.date.today()
        dif = self.valid_until - today
        return True if dif.days > 0 else False


class Promo2(models.Model):
    """
    Si compras 2+ de esta <categ> llevate gratis este <prod>
    <categ> es la categ con menos venta
    <prod> es un prod definido por el admin
    """
    product = models.ForeignKey(Product)
    category = models.ForeignKey(Category, blank=True, null=True)

    def save(self, *args, **kwargs):
        from stats import stats

        if not self.category:
            self.category = stats.category_less_sold()
        super(Promo2, self).save(*args, **kwargs)
