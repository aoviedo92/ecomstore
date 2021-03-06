# coding=utf-8
from django import forms
from models import Order
import datetime
import re
import locale  # para que los meses salgan en esp


def cc_expire_years():
    current_year = datetime.datetime.now().year
    years = range(current_year, current_year + 12)
    return [(str(x), str(x)) for x in years]


def cc_expire_months():
    locale.setlocale(locale.LC_TIME, '')  # para que los meses salgan en esp
    months = []
    for month in range(1, 13):
        if len(str(month)) == 1:
            numeric = '0' + str(month)
        else:
            numeric = str(month)
        months.append((numeric, datetime.date(2009, month, 1).strftime('%B').capitalize()))
    return months


CARD_TYPES = (('GOVMBA', 'GOVMBA Card'),)


def strip_non_numbers(data):
    """ gets rid of all non-number characters """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)


# Gateway test credit cards won't pass this validation
def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that the card passes a luhn mod-10 checksum """
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not ((count & 1) ^ oddeven):
            digit *= 2
        if digit > 9:
            digit -= 9
        sum += digit
    return (sum % 10) == 0


class CheckoutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        # override default attributes
        # for field in self.fields:
        #     self.fields[field].widget.attrs['size'] = '30'
        self.fields['credit_card_type'].widget.attrs['size'] = '1'
        self.fields['credit_card_expire_year'].widget.attrs['size'] = '1'
        self.fields['credit_card_expire_month'].widget.attrs['size'] = '1'
        self.fields['credit_card_cvv'].widget.attrs['size'] = '5'

    class Meta:
        model = Order
        exclude = ('status', 'ip_address', 'user', 'transaction_id', 'order_total')

    credit_card_number = forms.CharField(label=u"Número de crédito")
    credit_card_type = forms.CharField(widget=forms.Select(choices=CARD_TYPES), label="Tipo de tarjeta")
    credit_card_expire_month = forms.CharField(widget=forms.Select(choices=cc_expire_months()),
                                               label="Mes en que expira")
    credit_card_expire_year = forms.CharField(widget=forms.Select(choices=cc_expire_years()),
                                              label=u"Año en que expira")
    credit_card_cvv = forms.CharField(label="CVV")
    # ci = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Carnet de identidad'}), required=False)

    def clean_shipping_city(self):
        shipping_city = self.cleaned_data.get("shipping_city")
        if shipping_city == 0:
            raise forms.ValidationError("Debes escoger tu municipio")
        return shipping_city

        # def clean_credit_card_number(self):
        #     cc_number = self.cleaned_data['credit_card_number']
        #     stripped_cc_number = strip_non_numbers(cc_number)
        #     if not cardLuhnChecksumIsValid(stripped_cc_number):
        #         raise forms.ValidationError('The credit card you entered is invalid.')

        # def clean_phone(self):
        #     phone = self.cleaned_data['phone']
        #     stripped_phone = strip_non_numbers(phone)
        #     if len(stripped_phone) < 10:
        #         raise forms.ValidationError('Enter a valid phone number with area code.(e.g.555-555-5555)')
        #     return self.cleaned_data['phone']
