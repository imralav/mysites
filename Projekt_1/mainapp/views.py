#-*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import logout
from django.db.models.aggregates import Count
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from mainapp.forms import UserForm, ProfilForm, NewsForm, WyboryForm
from mainapp.models import Wybory, Glos, Profil, News, Kandydat


# Create your views here.
def index(request):
    context = RequestContext(request)

    posty = News.objects.filter(data_dodania__lte=datetime.now).order_by('-data_dodania')

    return render_to_response('mainapp/index.html', {'posty': posty}, context)

def addNews(request):
    context = RequestContext(request)

    if request.method == 'POST':
        news_form = NewsForm(data=request.POST)

        if news_form.is_valid():
            news = news_form.save(commit=False)
            news.save()

            return HttpResponseRedirect('/wybory/')
        else:
            print news_form.errors
    else:
        news_form = NewsForm()

    return render_to_response('mainapp/addNews.html', {'news_form': news_form}, context)

def editNews(request,whichId):
    context = RequestContext(request)
    newsInstance=News.objects.get(id__exact=whichId)
    if request.method == 'POST':
        news_form = NewsForm(request.POST,instance=newsInstance)

        if news_form.is_valid():
            news = news_form.save(commit=False)
            news.save()

            return HttpResponseRedirect('/wybory/')
        else:
            print news_form.errors
    else:
        news_form = NewsForm(instance=newsInstance)

    return render_to_response('mainapp/editNews.html', {'news_form': news_form, 'whichId': whichId}, context)


def delNews(request, whichId):
    News.objects.get(id = whichId).delete()
    return HttpResponseRedirect('/wybory/')


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = ProfilForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            profile_form.save_m2m()


            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = ProfilForm()

    # Render the template depending on the context.
    return render_to_response(
            'mainapp/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username andreturn  password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/wybory/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Yours Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('mainapp/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/wybory/')

@login_required
def user_wybory(request, user_name):
    context = RequestContext(request)
    usr = User.objects.filter(username = user_name)
    if usr is not None:
        profil = Profil.objects.get(user = usr)
        if profil is not None:
            glosy = Glos.objects.filter(glosujacy = profil).order_by('-wybory')

    dane = {}

    for g in glosy:
        dane[g.wybory] = Glos.objects.filter(glosujacy = profil, wybory = g.wybory)

    print dane
    context_dict = {'dane': dane, 'glosy': glosy, 'profil': profil}


    return render_to_response("mainapp/twojewybory.html", context_dict, context)

def newest(request):
    context = RequestContext(request)
    wybory = Wybory.objects.order_by('-poczatek')[:3]
    context_dict = {'wybory': wybory}
    return render_to_response("mainapp/newest.html", context_dict, context)

def lista(request, ile=None):
    context = RequestContext(request)
    if ile is None:
        wybory = Wybory.objects.order_by('-poczatek')
    else:
        wybory = Wybory.objects.order_by('-poczatek')[:ile]
    context_dict = {'wybory': wybory }
    return render_to_response("mainapp/lista.html", context_dict, context)

def addWybory(request):
    context = RequestContext(request)

    if request.method == 'POST':
        wybory_form = WyboryForm(data=request.POST)

        if wybory_form.is_valid():
            news = wybory_form.save(commit=False)
            news.ktoStworzyl = request.user
            news.zamkniete = False
            news.save()
            wybory_form.save_m2m()


            return HttpResponseRedirect('/wybory/details/'+str(news.id))
        else:
            print wybory_form.errors
    else:
        wybory_form = WyboryForm()

    return render_to_response('mainapp/addWybory.html', {'wybory_form': wybory_form}, context)

def editWybory(request, whichId):
    context = RequestContext(request)
    wyboryInstance=Wybory.objects.get(id__exact=whichId)
    if request.method == 'POST':
        wybory_form = WyboryForm(request.POST,instance=wyboryInstance)

        if wybory_form.is_valid():
            news = wybory_form.save(commit=False)
            news.save()

            return HttpResponseRedirect('/wybory/details/'+str(whichId))
        else:
            print wybory_form.errors
    else:
        wybory_form = WyboryForm(instance=wyboryInstance)

    return render_to_response('mainapp/editWybory.html', {'wybory_form': wybory_form, 'whichId': whichId}, context)

def delWybory(request, whichId):
    Wybory.objects.get(pk=whichId).delete()
    return HttpResponseRedirect('/wybory/lista')

def closeWybory(request, whichId):
    wybory = Wybory.objects.get(pk=whichId)
    wybory.zamkniete = True
    wybory.save()
    return HttpResponseRedirect('/wybory/lista')

def openWybory(request, whichId):
    wybory = Wybory.objects.get(pk=whichId)
    wybory.zamkniete = False
    wybory.save()
    return HttpResponseRedirect('/wybory/lista')

def wybory(request, wyboryId):
    context = RequestContext(request)
    wybory = Wybory.objects.get(pk=wyboryId)
    creatorProfile = Profil.objects.get(user = wybory.ktoStworzyl)

    context_dict = {'wybory': wybory, 'creator': creatorProfile}
    return render_to_response("mainapp/wybory.html", context_dict, context)

def glosuj(request, wyboryId):
    context = RequestContext(request)
    usr = User.objects.filter(username = request.user.username)
    _profil = Profil.objects.get(user = usr)
    wybory = Wybory.objects.get(pk=wyboryId)
    blad = False
    goodzawod = False
    error_msg = ""
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        wybrani = request.POST.getlist('kandydat')
        print wybrani
        print len(wybrani)
        print wybory.ilosc_wyborow
        if len(wybrani) > wybory.ilosc_wyborow:
            blad = True
            error_msg = " Można wybrać jedynie "+str(wybory.ilosc_wyborow)+" kandydatów! "
            return render_to_response('glosuj.html',{'wybory': wybory, 'blad': blad, 'error': error_msg}, context)

        for w in wybrani:
            kandydat = Kandydat.objects.get(pk=int(w))
            glos = Glos()
            glos.wybory = wybory
            glos.glosujacy = _profil
            glos.kandydat = kandydat
            glos.save()

        return render_to_response('mainapp/glosuj.html',{'wybory': wybory}, context)
    else:
        kandydaci = Kandydat.objects.filter(wybory__id=wybory.id)
        if wybory.poczatek > datetime.date(datetime.now()):
            error_msg+=" Jeszcze nie można głosować w tych wyborach. "
            blad = True
            context_dict = {'blad': blad, 'error': error_msg, 'wybory': wybory, 'kandydaci': kandydaci}
            return render_to_response('mainapp/glosuj.html', context_dict, context)

        if Glos.objects.filter(wybory=Wybory.objects.get(pk=wyboryId), glosujacy=_profil):
            error_msg+=" Głosowałeś już w tych wyborach. "
            blad = True
            context_dict = {'blad': blad, 'error': error_msg, 'wybory': wybory, 'kandydaci': kandydaci}
            return render_to_response('mainapp/glosuj.html', context_dict, context)

        if datetime.date(datetime.now()) > wybory.koniec:
            error_msg+=" Nie można już głosować w tych wyborach. "
            blad = True

        if datetime.now().year - _profil.data_urodzenia.year < wybory.wymagany_wiek:
            error_msg+=" Za mało lat. "
            blad = True

        if wybory.wymagana_niekaralnosc == True and _profil.karany == True:
            error_msg+=" Wymagana niekaralność. "
            blad= True

        for z in _profil.zawod.all():
            if z in wybory.wymagane_zawody.all():
                goodzawod = True
                break

        if not goodzawod:
            blad = True
            error_msg+=" Brak wymaganego zawodu. "

        context_dict = {'blad': blad, 'error': error_msg, 'wybory': wybory, 'kandydaci': kandydaci}
        return render_to_response('mainapp/glosuj.html', context_dict, context)

def wyniki(request, whichId):
    context = RequestContext(request)
    wybory = Wybory.objects.get(pk=whichId)
    wyniki = Glos.objects.filter(wybory=whichId).values('kandydat').annotate(dcount=Count('kandydat')).order_by('-dcount')
    for g in wyniki:
        g['kandydat'] = Kandydat.objects.get(pk=g['kandydat'])
    context_dict = {'wyniki': wyniki, 'wybory': wybory}

    print wyniki

    return render_to_response('mainapp/wyniki.html', context_dict, context)

def addCandidate(request):
    _user = User.objects.get(username=request.user.username)
    profil = Profil.objects.get(user=_user)
    kandydat = Kandydat()
    kandydat.profil = profil
    kandydat.save()
    context = RequestContext(request)

    return render_to_response('mainapp/addCandidate.html', {'message': "Gratulacje, zostałeś kandydatem!"}, context)

def profile(request, profileUsername):
    context = RequestContext(request)
    _user = User.objects.get(username=profileUsername)
    _profil = Profil.objects.get(user=_user)
    wybory = Wybory.objects.filter(ktoStworzyl=_user).order_by('-poczatek')
    glosy = Glos.objects.filter(glosujacy=_profil).order_by('-id')[:5]
    kandydat = Kandydat.objects.filter(profil=_profil)
    print kandydat
    return render_to_response('mainapp/profile.html', {'profil': _profil, 'wybory': wybory, 'glosy': glosy, 'czyKandydat': kandydat}, context)
