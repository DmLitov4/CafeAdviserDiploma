import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .models import Cities, Cuisine, Kind, Cafe, Areaplace, Photo

class CriteriaForm(forms.Form):

    kind = forms.ModelMultipleChoiceField(
        queryset = Kind.objects.all(), 
        widget  = forms.CheckboxSelectMultiple,
        label = ""
    )
    city = forms.ModelChoiceField(
        queryset = Cities.objects.all(),
        widget = forms.Select(),
        label = "",
        initial=0
    )
    area = forms.ModelMultipleChoiceField(
        queryset = Areaplace.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label = "",
        required=False
    )
    cuisine = forms.ModelMultipleChoiceField(
        queryset = Cuisine.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        label = "",
        required=False
    )
    parking = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[(1, "Да"), (2, "Нет"), (3, "Неважно")],
        label="",
        required=False
    )
