# from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
from ecomstore import settings

urlpatterns = patterns('checkout.views',
                       url(r'^$', 'show_checkout',
                           {'SSL': settings.ENABLE_SSL}, name='checkout'),

                       url(r'^receipt/$', 'receipt',
                           {'SSL': settings.ENABLE_SSL}, name='checkout_receipt'),

                       )
