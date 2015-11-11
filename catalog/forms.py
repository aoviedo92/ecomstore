# -*- coding: utf-8 -*-
from ecomstore import settings

__author__ = 'adrian'
from django import forms
from catalog.models import Product, ProductReview, ProductRating


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = []

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['price']


class ProductAddToCartForm(forms.Form):
    # quantity = forms.IntegerField(
    #     widget=forms.TextInput(attrs={'size': '2', 'value': '1', 'class': 'quantity', 'maxlength': '5'}),
    #     error_messages={'invalid': 'Please enter a valid quantity.'},
    #     min_value=1
    # )
    product_slug = forms.CharField(widget=forms.HiddenInput())

    # override the default __init__ so we can set the request
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    # custom validation to check for cookies
    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data


class OrderByForm(forms.Form):
    OPTIONS = (("created_at", "Fecha"), ("name", "Nombre"), ("price", "Precio"), ("brand", "Marca"),)
    order_by = forms.ChoiceField(choices=OPTIONS, label="Ordenar por")


class ProductsPerPageForm(forms.Form):
    products_x_page = settings.PRODUCTS_PER_PAGE
    offset = 6
    OPTIONS = []
    for i in [products_x_page, products_x_page + offset, products_x_page + offset * 2]:
        OPTIONS.append((i, str(i)))
    products_per_page = forms.ChoiceField(choices=OPTIONS, label="Mostrar", required=False)


class Currency(forms.Form):
    OPTIONS = (('cuc', 'CUC'), ('mn', 'MN'),)
    currency = forms.ChoiceField(choices=OPTIONS,
                                 label="",
                                 required=False,
                                 widget=forms.Select(
                                     attrs={"tabindex": 4, "class": "dropdown", "id": "id_currency_select"}))


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        exclude = ('user', 'product', 'is_approved', 'rating')

    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": u"Deja tu opinión si quieres", "class": "leave_msg"}), label="",
                              required=False)


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        exclude = ('user', 'product', 'is_approved', 'rating')

    rating = forms.IntegerField(widget=forms.HiddenInput())
