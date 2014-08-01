from django.contrib import admin

from mainapp.models import Kategoria, Zawod, Obywatelstwo, Wybory, \
    Profil, Glos, News, Kandydat


# Register your models here.
admin.site.register(Kategoria)
admin.site.register(Zawod)
admin.site.register(Obywatelstwo)
admin.site.register(Wybory)
admin.site.register(Profil)
admin.site.register(Glos)
admin.site.register(News)
admin.site.register(Kandydat)