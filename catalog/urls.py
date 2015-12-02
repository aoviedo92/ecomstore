from django.conf.urls import patterns, url
from catalog import views

urlpatterns = patterns('catalog.views',
                       url(r'^$', 'index', name='catalog_home'),
                       # url(r'^category/(?P<group_name>[-\w]+)/$', 'show_category', name='group_name'),
                       url(r'^category/common/(?P<common_name>[-\w]+)/$', 'show_category',
                           name='catalog_common_category'),
                       url(r'^category/(?P<category_slug>[-\w]+)/$', 'show_category', name='catalog_category'),
                       url(r'^product/(?P<product_slug>[-\w]+)/$', 'show_product', name='catalog_product'),
                       url(r'^currency/$', 'currency', name='currency'),
                       url(r'^catalog/quick-access/(?P<quick_access_slug>[-\w]+)/$', 'quick_access', name='quick_access'),
                       url(r'^rifas/$', 'rifas', name='rifas'),
                       url(r'^tag/(?P<tag_>[-\w]+)/$', 'tag', name='tag'),
                       url(r'^test_urllib/$', 'test_urllib', name='test_urllib'),
                       # ajax call
                       url(r'^review/product/add/$', 'add_review'),
                       url(r'^review/product/vote/$', 'add_vote'),
                       url(r'^wishlist/add/$', 'add_wish_list'),
                       url(r'^wishlist/remove/$', 'remove_wish_list'),
                       url(r'^tag/product/add/$', 'add_tag'),
                       )
# (?P<name_group>[-\w]+)/
