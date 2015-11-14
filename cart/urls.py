from django.conf.urls import patterns, url

urlpatterns = patterns('cart.views',
                       url(r'^$', 'show_cart', name='show_cart'),
                       url(r'^cart-add-list/$', 'add_to_cart_product_list', name='add_to_cart_product_list'),
                       url(r'^process-discount-code/$', 'ajax_test'),
                       )
