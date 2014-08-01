from django.conf.urls import patterns, url

from mainapp import views


urlpatterns = patterns('',
           url(r'^$', views.index, name='index'),
           url(r'^login/$', views.user_login, name='login'),
           url(r'^logout/$', views.user_logout, name='logout'),
           url(r'^register/$', views.register, name='register'), 
           
           url(r'^(?P<user_name>.+)/twojewybory/$', views.user_wybory, name='user_wybory'),
           url(r'^lista/(\d+)/$', views.lista, name='lista'),
           url(r'^lista/$', views.lista, name='lista'),
           url(r'^addWybory/$', views.addWybory, name='addWybory'),
           url(r'^editWybory/(\d+)/$', views.editWybory, name='editWybory'),
           url(r'^delWybory/(\d+)/$', views.delWybory, name='delWybory'),
           url(r'^closeWybory/(\d+)/$', views.closeWybory, name='closeWybory'),
           url(r'^openWybory/(\d+)/$', views.openWybory, name='openWybory'),
           url(r'^details/(\d+)/$', views.wybory, name='wybory'),
           url(r'^glosuj/(\d+)/$', views.glosuj, name='glosuj'),
           url(r'^wyniki/(\d+)/$', views.wyniki, name='wyniki'),
           url(r'^(.+)/profile/$', views.profile, name='wyniki'),
           
           url(r'^addnews/$', views.addNews),
           url(r'^delnews/(\d+)/', views.delNews),
           url(r'^editnews/(\d+)/', views.editNews),
           
           url(r'^addCandidate/$', views.addCandidate),
           
        )