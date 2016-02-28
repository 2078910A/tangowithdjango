from django.shortcuts import render
from django.http import HttpResponse, Http404
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
import random

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': category_list,
        'pages': page_list,
    }

    return render(request, 'rango/index.html', context_dict)

def about(request):

    descriptions = ["funny", "smart", "cool", "uncool"]

    context_dict = {'boldmessage': random.choice(descriptions)}

    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

        #used in the template to verify that the category exists
        context_dict['category'] = category

        context_dict['category_name_slug'] = category_name_slug

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #Have we been provided with a valid form?
        if form.is_valid():
            try:
                form.save(commit=True)
                return index(request)
            except:
                #Now call the index view, return the user to the homepage
                return index(request)
            ##return category(request, slugBeingChecked
        else:
            #The supplied form contained errors, print them to the console
            print form.errors

    else:
        #If the request was not a POST, display the form
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)