from django.conf.urls import patterns, include, url
from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wybory/', include('mainapp.urls')),
    url(r'^',include('mainapp.urls')),
)
