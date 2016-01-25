from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    context_dict = {'boldmessage' : 'Rango is a dick, though.'}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    return HttpResponse("Rango says here is the about page."
                        "<br/> The <a href='/rango/'>index page</a>")