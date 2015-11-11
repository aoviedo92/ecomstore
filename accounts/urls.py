from django.conf.urls import patterns, url
from ecomstore import settings

urlpatterns = patterns('accounts.views',
                       url(r'^register/$', 'register', {'SSL': settings.ENABLE_SSL}, name='register'),
                       url(r'^my_account/$', 'my_account', name='my_account'),
                       url(r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details', name='order_details'),
                       url(r'^order_info/$', 'order_info', name='order_info'),
                       url(r'^logout/$', 'log_out', name='logout'),
                       url(r'^my_account/wishlist/$', 'wish_list', name='wishlist'),
                       )
urlpatterns += patterns('django.contrib.auth.views',
                        url(r'^login/$', 'login',
                            {'template_name': 'registration/login.html', 'SSL': settings.ENABLE_SSL}, 'login'),
                        )
