from django.conf.urls import patterns, include, url
from django.contrib import admin
from ecomstore import settings
from django.views.generic import DetailView, ListView, TemplateView

urlpatterns = patterns('',
                       url(r'^catalog/', include('catalog.urls')),
                       url(r'^', include('catalog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^cart/', include('cart.urls')),
                       url(r'^checkout/', include('checkout.urls')),
                       url(r'^accounts/', include('accounts.urls')),
                       url(r'^accounts/', include('django.contrib.auth.urls')),
                       url(r'^search/', include('search.urls')),
                       url(r'^manager/', include('manager.urls')),

                       url(r'^quienes-somos/$', TemplateView.as_view(template_name='flatpages/about_us.html'), name='about_us'),
                       url(r'^cookies-policy/$', TemplateView.as_view(template_name='flatpages/cookies.html'), name='cookies'),
                       url(r'^faq/$', TemplateView.as_view(template_name='flatpages/faq.html'), name='faq'),
                       url(r'^payments/$', TemplateView.as_view(template_name='flatpages/payments.html'), name='payments'),
                       url(r'^privacity/$', TemplateView.as_view(template_name='flatpages/privacity.html'), name='privacity'),
                       url(r'^returns/$', TemplateView.as_view(template_name='flatpages/returns.html'), name='returns'),
                       url(r'^shopping/$', TemplateView.as_view(template_name='flatpages/shopping.html'), name='shopping'),

                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),
                       )

handler404 = 'ecomstore.views.file_not_found_404'
