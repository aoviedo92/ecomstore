from django.conf.urls import patterns, url

urlpatterns = patterns('manager.views',
                       url(r'^promo3/$', 'promo3', name='promo3'),
                       url(r'^promo3_find_users/$', 'promo3_find_users'),
                       url(r'^promo3_random_users/$', 'promo3_random_users'),
                       url(r'^populate-categories/$', 'create_group_categories'),
                       url(r'^create_products/$', 'create_products'),
                       url(r'^send_mail/$', 'send_mail'),
                       )
