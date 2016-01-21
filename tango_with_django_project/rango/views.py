from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Rango says hello! "
                        "<br/> The <a href='/rango/about'>about page</a>")

def about(request):
    return HttpResponse("Rango says here is the about page."
                        "<br/> The <a href='/rango/'>index page</a>")