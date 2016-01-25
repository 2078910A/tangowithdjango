from django.shortcuts import render
from django.http import HttpResponse
import random

def index(request):

    context_dict = {'boldmessage' : 'Rango is a dick, though.'}

    return render(request, 'rango/index.html', context_dict)

def about(request):

    descriptions = ["funny", "smart", "cool", "uncool"]

    context_dict = {'boldmessage': random.choice(descriptions)}

    return render(request, 'rango/about.html', context_dict)