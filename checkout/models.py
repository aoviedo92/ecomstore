from django.db import models
from django import forms
from django.contrib.auth.models import User
from catalog.models import Product
from decimal import Decimal


class BaseOrderInfo(models.Model):
    # The abstract = True in the inner Meta class designates this model as a base class that will never get
    # its own data table, and should not normally be instantiated in our Python code.
    class Meta:
        abstract = True

    CITIES = [(0, "Seleccione municipio"), (1, "playa"), (2, "cerro"), (3, "lisa"), (4, "boyeros"), (5, "plaza"),
              (6, "arroyo naranjo"),
              (7, "cotorro"), (8, "marianao"), (9, "regla"), (10, "centro habana"), (11, "habana vieja"),
              (12, "habana del este"), (13, "10 de octubre"), (14, "guanabacoa"), (15, "san miguel")]

    # contact info
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    # shipping information
    shipping_name = models.CharField(max_length=50, verbose_name="Envio a nombre de")
    shipping_address_1 = models.CharField(max_length=50)
    shipping_address_2 = models.CharField(max_length=50, blank=True)
    shipping_city = models.IntegerField(choices=CITIES, max_length=50, default=0)


class OrderTotal(models.Model):
    shipping_tax = models.DecimalField(default=3.00, decimal_places=2, max_digits=9)
    discount = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    cart_subtotal = models.DecimalField(decimal_places=2, max_digits=9)
    purchased = models.BooleanField(default=False)

    @property
    def total(self):
        return Decimal(self.cart_subtotal) - Decimal(self.discount) + Decimal(self.shipping_tax)

    def __unicode__(self):
        return '%d -- %.2f' % (self.id, self.total)

class Order(BaseOrderInfo):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED, 'Submitted'),
                      (PROCESSED, 'Processed'),
                      (SHIPPED, 'Shipped'),
                      (CANCELLED, 'Cancelled'),)
    # order info
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField()
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    transaction_id = models.CharField(max_length=20)
    order_total = models.OneToOneField(OrderTotal)
    # shipping_tax = models.DecimalField(default=3.00)
    # discount = models.DecimalField(default=0.00)

    def __unicode__(self):
        return 'Order # %d -- %.2f' % (self.id, self.order_total.total)

    @property
    def total(self):
        # total = decimal.Decimal('0.00')
        # order_items = OrderItem.objects.filter(order=self)
        # for item in order_items:
        #     total += item.total
        return self.order_total.total

    @models.permalink
    def get_absolute_url(self):
        return 'order_details', (), {'order_id': self.id}


class OrderItem(models.Model):
    product = models.ForeignKey(Product)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order)

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.sku

    def __unicode__(self):
        return self.product.name + ' (' + self.product.sku + ')'

    def get_absolute_url(self):
        return self.product.get_absolute_url()
