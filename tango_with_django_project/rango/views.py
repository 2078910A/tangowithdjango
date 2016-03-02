from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
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


def register(request):

    #A boolean value for telling the template whether the registration was successful.
    #Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    #if it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        #Attempt to grab information from the raw form information
        #Note that we make use of both UserForm and UserProfileForm
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            #Save the user's form data to the database.
            user = user_form.save()

            #Now we hash the password with the set_password method
            #Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            #Now sort out the UserProfile instance.
            #Since we need to set the user attribute ourselves, we set commit=False.
            #This delays saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            #Did the user provide a profile piture?
            #If so we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #Now we save the UserProfile model instance
            profile.save()

            #Update our variable to tell the template regisitration was successful
            registered = True

        #Invalid form or forms - mistake or something else?
        #Print problems to the terminal
        #They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    #Not a HTTP POST, so we render our form using two ModelForm instances
    #These forms wil be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    #Render the template depending on context
    return render(request,
        'rango/register.html',
        {'user_form': user_form, 'profile_form': profile_form,
            'registered': registered})


def user_login(request):

    #if the request method is POST try to pull out the relevent info
    if request.method == 'POST':
        #Gather the username and password provided by the user
        #This info is obtained from the login form.
            #We use request.POST.get('<variable>') as opposed to just request.POST['<variable>']
            #because the  request.POST.get('<variable>') returns None if the value does not exist
            #whereas request.POST['<variable>'] would raise a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Use Django's machinery to see if the username/password combination is valid,
        #a User object is returned if so
        user = authenticate(username=username, password=password)

        #If we have a User object then the details are correct
        #If None (Python's way of representing the absence of a value) no user
        #with matching credentials was found.
        if user:
            #Check the user is still active (not banned)
            if user.is_active:
                #If the account is valid and active then we can log the user in
                #We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                #An inactive(banned) account was used, no logging in!
                return HttpResponse("Your Rango account is disabled")
        else:
            #Bad login details were provided so we can't log the user in
            print "Ivalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        #The request is not an HTTP POST, so display the login form
        #This scenario would most likely be an HTTP GET
        return render(request, 'rango/login.html', {})


@login_required
def restricted(request):
    return HttpResponse("Since you are logged in, you can see this text!")


#Use the @login_required decorator to make sure only those that are logged in can log out!
@login_required
def user_logout(request):
    #Since we know the user is logged in we can just log them out
    logout(request)

    #Take the user back to the homepage
    return HttpResponseRedirect('/rango/')