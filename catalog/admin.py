from django.contrib import admin

# Register your models here.
from django.contrib import admin
from catalog.models import Product, Category, CategoryGroup, Images, CommonCategory, ProductReview, ProductRating
from catalog.forms import ProductAdminForm


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'old_price', 'created_at', 'slug',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ('created_at', 'updated_at',)
    # sets up slug to be generated from product name
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    # sets up values for how admin site lists categories
    list_display = ('name', 'slug',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug': ('name',)}


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'date', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user', 'content', 'title']


class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'date', 'rating')
    list_per_page = 20
    list_filter = ('product', 'user')
    ordering = ['date']
    search_fields = ['user', 'content', 'title']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CategoryGroup)
admin.site.register(CommonCategory)
admin.site.register(Images)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductRating, ProductRatingAdmin)
