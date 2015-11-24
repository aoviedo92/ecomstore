from django.contrib import admin
from models import Order, OrderItem, OrderTotal


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    # we have the option of leaving empty forms on the page, so that new OrderItems can be created for
    # the Order. Because we don't need this functionality, we've also set the extra field to zero.
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'date', 'status', 'transaction_id', 'user')
    list_filter = ('status', 'date')
    search_fields = ('email', 'shipping_name', 'id', 'transaction_id')
    inlines = [OrderItemInline, ]
    fieldsets = (
        ('Basics', {'fields': ('status', 'email', 'phone')}),
        ('Shipping', {'fields': ('shipping_name', 'shipping_address_1',
                                 'shipping_address_2', 'shipping_city',
                                 )}),
        # ('Billing', {'fields': ('billing_name', 'billing_address_1',
        #                         'billing_address_2', 'billing_city',)})

    )


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderTotal)
