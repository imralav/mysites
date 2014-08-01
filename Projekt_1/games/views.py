from django.shortcuts import render_to_response
from django.template.context import RequestContext

# Create your views here.

def index(request):
    context = RequestContext(request)

    return render_to_response('games/index.html', {}, context)

def staroverflow(request):
    context = RequestContext(request)
    
    return render_to_response('games/staroverflow.html', {}, context)