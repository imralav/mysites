#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

from mainapp.models import Profil, News, Wybory
from django.forms.widgets import HiddenInput


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label=u"Hasło")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfilForm(forms.ModelForm):
    data_urodzenia = forms.DateField(widget=SelectDateWidget(years=range(1920,2014)));

    class Meta:
        model = Profil
        fields = ('imie','nazwisko','data_urodzenia','zawod','karany','obywatelstwo')

class NewsForm(forms.ModelForm):
    data_dodania = forms.DateField(widget=SelectDateWidget);

    class Meta:
        model = News

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['tresc'].widget.attrs['cols'] = 100
        self.fields['tresc'].widget.attrs['rows'] = 25

class WyboryForm(forms.ModelForm):
    poczatek = forms.DateField(widget=SelectDateWidget)
    koniec = forms.DateField(widget=SelectDateWidget)
    #ktoStworzyl = forms.IntegerField(widget=HiddenInput, initial=0)

    class Meta:
        model = Wybory
        fields = ('tytul', 'opis', 'kategoria', 'poczatek', 'koniec', 'wymagane_zawody', 'ilosc_wyborow', 'wymagany_wiek', 'wymagana_niekaralnosc', 'kandydaci')

