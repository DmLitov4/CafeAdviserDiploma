from django.shortcuts import render
from login.forms import *
from login.models import *
from cafe.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            first_name=form.cleaned_data['firstname'],
            last_name=form.cleaned_data['lastname'],
            email=form.cleaned_data['email']
            )
            u = User.objects.get(username=form.cleaned_data['username'])
            c = Cities.objects.get(cityname=form.cleaned_data['city'])
            usersetting = UserSettings.objects.create(
            user = u,
            age=form.cleaned_data['age'],
            gender=form.cleaned_data['gender'],
            city=c.cityname,
            avatar = form.cleaned_data['image']
            )
            usersetting.save()
            return HttpResponseRedirect('success/')
        else:
            print("Wrong!")
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

def login_page(request):
    try:
        remember = request.POST['remember_me']
        if remember:
            print("remembered...")
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        else:
            print("not remembered...")
    except:
            is_private = False
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
            print("exception...")
    print("all right now...")
    login(request)
    return HttpResponseRedirect('/')
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    return render_to_response(
    'home.html',
    { 'user': request.user }
    )