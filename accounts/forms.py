# coding=utf-8
from django import forms
from django.contrib.auth.models import User
from models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    override init para poner un attr a email(value) si este lo lleva
    """
    def __init__(self, email_from_user=None, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if email_from_user:
            self.fields['email'].widget.attrs['value'] = email_from_user

    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Apellidos'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Teléfono'}))
    shipping_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enviado a nombre de'}))
    shipping_address_1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enviar a esta dirección'}))
    shipping_address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enviado a esta dirección opcional'}))
    # birth_day = forms.DateField(input_formats='%d/%m/%Y',
    #                             widget=forms.DateInput(attrs={'placeholder': 'Fecha de nacimiento'}))

    class Meta:
        model = UserProfile
        exclude = ('user', 'wish_list')
        # fields = ('phone', 'shipping_name', 'shipping_address_1', 'shipping_address_2', 'shipping_city', 'sex',
        #           )
        # NO validamos para q el usuario si no quiere, no registre estos datos
        # def clean_sex(self):
        #     sex = self.cleaned_data.get("sex")
        #     if sex == 0:
        #         raise forms.ValidationError("Debes escoger tu sexo")
        #     return sex

        # def clean_shipping_city(self):
        #     shipping_city = self.cleaned_data.get("shipping_city")
        #     if shipping_city == 0:
        #         raise forms.ValidationError("Debes escoger tu municipio")
        #     return shipping_city


class UserCreationForm(forms.ModelForm):
    error_messages = {
        # 'duplicate_username': "A user with that username already exists.",
        'password_mismatch': "Los passwords deben coincidir",
    }
    username = forms.RegexField(label="Nombre", max_length=30,
                                regex=r'^[\w.@+-]+$',
                                widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'}),
                                error_messages={
                                    'invalid': u"Debe contener solo letras, números y los caracteres @/./+/-/_."})
    password1 = forms.CharField(label="Password",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="Confirmar password",
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Password'}),
                                )

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length="50", widget=forms.TextInput(attrs={'placeholder': 'Email'}))
