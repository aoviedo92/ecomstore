from django.conf.urls import patterns, url

urlpatterns = patterns('manager.views',
                       url(r'^populate-categories/$', 'create_group_categories'),
                       url(r'^create_products/$', 'create_products'),
                       )
rifas_pattern = patterns('manager.rifas',
                         url(r'^rifas/add-user/$', 'add_user_rifas'),
                         url(r'^rifas/remove-user/$', 'remove_user_rifas'),
                         url(r'^rifas/retrieve-info/$', 'retrieve_info'),
                         url(r'^rifas/rifas-results/$', 'rifas_results'),
                         url(r'^rifas/get-winner-user/$', 'get_winner_user'),
                         )
promo3_pattern = patterns('manager.promo3',
                          url(r'^promo3/$', 'promo3', name='promo3'),
                          url(r'^promo3_find_users/$', 'promo3_find_users'),
                          url(r'^promo3_random_users/$', 'promo3_random_users'), )
urlpatterns += rifas_pattern + promo3_pattern
