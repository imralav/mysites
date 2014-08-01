from Projekt_1.views import index
from django.conf.urls import patterns, include, url
from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wybory/', include('mainapp.urls')),
    url(r'^games/', include('games.urls')),
    url(r'^',index),
)
