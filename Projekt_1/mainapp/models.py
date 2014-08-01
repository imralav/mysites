#-*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models



# TODO:
# do wyborow dodac nazwe, kto utworzyl
# Create your models here.
class Kategoria(models.Model):
    nazwa = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural="Kategorie"

    def __unicode__(self):
        return self.nazwa

class Zawod(models.Model):
    nazwa = models.CharField(max_length = 50)

    class Meta:
        verbose_name_plural=u"Zawód"
        verbose_name_plural=u"Zawody"

    def __unicode__(self):
        return self.nazwa

class Obywatelstwo(models.Model):
    kraj = models.CharField(max_length = 50)

    class Meta:
        verbose_name_plural="Obywatelstwa"

    def __unicode__(self):
        return self.kraj

class Profil(models.Model):
    user = models.OneToOneField(User)
    imie = models.CharField(max_length=25, verbose_name=u"Imię")
    nazwisko = models.CharField(max_length=100)
    data_urodzenia = models.DateField()
    zawod = models.ManyToManyField(Zawod, verbose_name=u"Zawód")
    karany = models.BooleanField(default=False)
    obywatelstwo = models.ManyToManyField(Obywatelstwo)

    class Meta:
        verbose_name_plural=u"Profile"

    def __unicode__(self):
        return u"%s %s" % (self.nazwisko, self.imie)

class Kandydat(models.Model):
    profil = models.OneToOneField(Profil)


    class Meta:
        verbose_name_plural=u"Kandydaci"

    def __unicode__(self):
        return u"%s %s" % (self.profil.nazwisko, self.profil.imie)

class Wybory(models.Model):
    tytul = models.CharField(max_length=25, verbose_name=u"Tytuł")
    opis = models.TextField()
    kategoria = models.ForeignKey(Kategoria)
    poczatek = models.DateField(verbose_name=u"Początek")
    koniec = models.DateField(verbose_name=u"Koniec")
    ilosc_wyborow = models.IntegerField(default=1, verbose_name=u"Ilość wyborów")
    wymagany_wiek = models.IntegerField(default=18, verbose_name=u"Wymagany wiek")
    wymagane_zawody = models.ManyToManyField(Zawod, verbose_name=u"Wymagane zawody")
    wymagana_niekaralnosc = models.BooleanField(default=True, verbose_name=u"Wymagana niekaralność")
    kandydaci = models.ManyToManyField(Kandydat)
    ktoStworzyl = models.ForeignKey(User)
    zamkniete = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Wybory"

    def __unicode__(self):
        return u'W. %s "%s"' % (self.kategoria, self.tytul)

    def __hash__(self):
        return hash((self.tytul, self.ktoStworzyl, self.poczatek, self.koniec))

    def __eq__(self, other):
        return (self.tytul, self.ktoStworzyl, self.poczatek, self.koniec) == (other.tytul, other.ktoStworzyl, other.poczatek, other.koniec)

class Glos(models.Model):
    glosujacy = models.ForeignKey(Profil, related_name="id_glosujacego")
    kandydat = models.ForeignKey(Kandydat, related_name="id_kandydata")
    wybory = models.ForeignKey(Wybory)

    class Meta:
        verbose_name_plural="Glosy"


    def __unicode__(self):
        return u'%s %s na %s %s w wybory %s "%s"' % (self.glosujacy.nazwisko,self.glosujacy.imie,self.kandydat.profil.nazwisko,self.kandydat.profil.imie, self.wybory.kategoria.nazwa, self.wybory.tytul)

class News(models.Model):
    tytul = models.CharField(max_length = 50, verbose_name=u"Tytuł")
    tresc = models.TextField(verbose_name=u"Treść")
    data_dodania = models.DateField(verbose_name=u"Data dodania")

    class Meta:
        verbose_name_plural="Newsy"

    def __unicode__(self):
        return u"%s" % self.tytul