# coding=utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Avg
from django.template.defaultfilters import slugify, truncatewords, capfirst
from django.utils import timezone
import tagging
from tagging.registry import register as register_tag_for, AlreadyRegistered


class ActiveManager(models.Manager):
    """
    Manager class to return only those products where each instance is active
    """

    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class CategoryGroup(models.Model):
    group_name = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('catalog_category_group', kwargs={'group_name': self.group_name})

    def __unicode__(self):
        return self.group_name


class CommonCategory(models.Model):
    common_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.common_name

    def get_absolute_url(self):
        return reverse('catalog_common_category', kwargs={'common_name': self.common_name})


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    # groups = models.ManyToManyField(CategoryGroup, null=True)
    group = models.ForeignKey(CategoryGroup, null=True, blank=True)
    common = models.ForeignKey(CommonCategory, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # filter_name = models.ManyToManyField(Filter, blank=True)
    SEX = ((0, 'Ambos'), (1, 'Femenino'), (2, 'Masculino'),)
    sex = models.IntegerField(choices=SEX, default=0)
    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog_category', kwargs={'category_slug': self.slug})

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Images(models.Model):
    image = models.ImageField(upload_to='images/products/secondary')

    def __unicode__(self):
        return self.image.name


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    brand = models.CharField(max_length=50, default="brand")
    sku = models.CharField(max_length=50, default="sku")
    price = models.DecimalField(max_digits=9, decimal_places=2, default=200)
    old_price = models.DecimalField(max_digits=9, decimal_places=2, blank=True, default=0.00)
    image = models.ImageField(upload_to='images/products/main')
    second_images = models.ManyToManyField(Images, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    quantity = models.IntegerField(default=30)

    description = models.TextField(default="""Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy
                            nibh
                            euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim
                            veniam,
                            quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo
                            consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie
                            consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto
                            odio
                            dignissim qui blandit""")

    meta_keywords = models.CharField(max_length=255, default="meta",
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField(max_length=255, default="meta", help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog_product', kwargs={'product_slug': self.slug})

    def sale_price(self):
        if self.old_price > self.price:
            return self.price
        else:
            return None

    def great_sales(self):
        percent = 0
        if self.sale_price():
            percent = 100 - self.price * 100 / self.old_price
        return True if percent >= 45 else False

    def new_product(self):
        days_product_is_new = 5
        now = timezone.now()
        delta = now - self.created_at
        return True if delta.days < days_product_is_new else False

    def cross_sell(self):
        """
        Otros productos que se vendieron junto con este
        """
        # importar aqui y no al top of file para evitar imports ciclicos, pq OrderItem importa Products
        from checkout.models import Order, OrderItem

        orders = Order.objects.filter(orderitem__product=self)  # todas las orders que tuvieron este producto
        # print("orders", orders)
        order_items = OrderItem.objects.filter(
            order__in=orders).exclude(product=self)  # cada item de esas orders, sin contrar este producto
        # print("order_items", order_items)
        products = Product.active.filter(orderitem__in=order_items).distinct()  # product de esos order items
        # print("product", products)
        return products

    def cross_tags(self):
        """
        productos relacionados segun sus tags.
        hay coincidencia si las tags del self se encuantran en otros prod por encima de un 70% y si la cant de tags
        entre ambos no se exceden mas de la mitad del que mayor tags tenga. de esta forma aseguramos q ambos prod sean
        bastante semejantes.
        """
        self_categories = self.categories.all()
        products = Product.active.all()
        self_categories_count = self_categories.count()
        products_cross_tags = []
        for product in products:
            cat_match = 0
            if product != self:
                categories = product.categories.all()
                for cat in categories:
                    if cat in self_categories:
                        cat_match += 1
                percent = 100 * cat_match / self_categories_count
                if percent < 66:  # producto bien relacionado, bastante similar
                    continue
                if self_categories_count > categories.count():
                    if self_categories_count / 2 > categories.count():
                        continue
                if self_categories_count < categories.count():
                    if self_categories_count < categories.count() / 2:
                        continue
                products_cross_tags.append(product)
        return products_cross_tags

    def discounts(self):
        products = Product.active.all()
        prod_discounts = []
        for prod in products:
            if prod.sale_price():
                prod_discounts.append(prod)
        print("discounts", prod_discounts)
        return prod_discounts

    def avg_rating(self):
        try:
            avg_rating = ProductRating.objects.filter(product=self).aggregate(Avg('rating'))['rating__avg']
            avg_rating = int(avg_rating)
        except TypeError:
            avg_rating = 0
        return avg_rating

    def tooltip(self):
        product_already_voted = ProductRating.objects.filter(product=self)
        desc = capfirst(truncatewords(self.description, 25))
        no_voted = u"No ha sido valorada aún"
        # no_voted = u"No ha sido valorada aún"
        avg = self.avg_rating() if product_already_voted else no_voted
        comments = ProductReview.approved.filter(product=self).count()
        tooltip = u"<p style='color:#777;font-size:0.85em;line-height:1.8em;border-bottom:1px solid #999'>%s</p>" \
                  u"<span style='color:#333;font-size:0.95em;line-height:2em;padding:10px;'>Valoración:</span> " \
                  u"<span style='color:#999;font-size:0.70em;line-height:1.8em;'>%s</span></br>" \
                  u"<span style='color:#333;font-size:0.95em;line-height:2em;padding:10px;'>Comentarios:</span> " \
                  u"<span style='color:#999;font-size:0.70em;line-height:1.8em;'>%s</span>" % (desc, avg, comments)
        return tooltip

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


try:
    register_tag_for(Product)
except AlreadyRegistered:
    pass


class ActiveProductReviewManager(models.Manager):
    # def all(self):
    #     return super(ActiveProductReviewManager, self).all().filter(is_approved=True)
    def get_queryset(self):
        return super(ActiveProductReviewManager, self).get_queryset().filter(is_approved=True, content__gt=0)


class Review(models.Model):
    class Meta:
        abstract = True

    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)


class ProductReview(Review):
    is_approved = models.BooleanField(default=True)
    content = models.TextField(blank=True)
    objects = models.Manager()
    approved = ActiveProductReviewManager()

    def __unicode__(self):
        return self.content


class ProductRating(Review):
    rating = models.IntegerField(default=3)

    def __unicode__(self):
        return "%s - %s " % (str(self.product), str(self.rating))


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

        category = stats.category_less_sold()
        self.category = category
        super(Promo2, self).save(*args, **kwargs)
