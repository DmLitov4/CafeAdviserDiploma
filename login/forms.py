import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from cafe.models import *
 
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Логин:"), error_messages={'required': 'Поле обязательно для заполнения', 'invalid': _("Поле должно содеражть только буквы, цифры и нижние подчеркивания") })
    firstname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)), label=_("Имя: "), error_messages={'required': 'Поле обязательно для заполнения', 'invalid': _('Данное имя недопустимо')})
    lastname = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=100)), label=_("Фамилия: "), error_messages={'invalid': _("Данная фамилия недопустима") })
    age = forms.IntegerField(min_value=16, label=_("Возраст: "), error_messages={'min_value':'Возраст должен быть не меньше 16 лет'})
    gender= forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[("М", "М"), ("Ж", "Ж")],
        label="Пол: ",
        required=True
    )
    city = forms.ModelChoiceField(
        queryset = Cities.objects.all(),
        widget = forms.Select(),
        label = "Город: ",
        initial=0
    )
    image = forms.ImageField()
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email:"), error_messages={'required': 'Поле обязательно для заполнения'})
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Пароль:"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Пароль ещё раз:"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("Пользователь с таким именем уже существует! Попробуйте ещё раз."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Введенные пароли не совпадают"))
        return self.cleaned_data

class LoginForm(forms.Form): 
     
     username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Логин:"), error_messages={ 'invalid': _("Поле должно содеражть только буквы, цифры и нижние подчеркивания") })
     password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Пароль:")) 
     remember_me = forms.NullBooleanField() 

     user_cache = None

