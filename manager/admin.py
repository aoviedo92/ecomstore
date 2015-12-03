from django.contrib import admin
from manager.models import Promo2, Promo3, Promo4


class Promo4ModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)
    list_display = ('__unicode__', 'active', 'winner_user')
    # filter_horizontal = ('users',)


admin.site.register(Promo2)
admin.site.register(Promo3)
admin.site.register(Promo4, Promo4ModelAdmin)
