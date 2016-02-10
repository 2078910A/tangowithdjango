from django.shortcuts import render
from django.http import HttpResponse, Http404
from rango.models import Category, Page
import random

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories' : category_list,
        'pages' : page_list,
    }

    return render(request, 'rango/index.html', context_dict)

def about(request):

    descriptions = ["funny", "smart", "cool", "uncool"]

    context_dict = {'boldmessage': random.choice(descriptions)}

    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_url):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_url)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

        #used in the template to verify that the category exists
        context_dict['category'] = category

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

