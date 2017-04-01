from django.shortcuts import render
from login.forms import *
from login.models import *
from cafe.models import *
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
import numpy as np
import vk, time, operator
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob

session = vk.Session(access_token=settings.VK_TOKEN)
api = vk.API(session)

def vk_clasterization(request):
    users = UserSettings.objects.all()
    print('selecting users...')
    with open('trainmusic.csv', 'r') as fp:
        cl = NaiveBayesClassifier(fp, format="csv")
    for u in users:
        query_string = u.user.first_name + ' ' + u.user.last_name
        print(query_string)
        query_array = api.users.search(q=query_string, age_from=u.age, age_to=u.age, hometown=u.city, count=1, fields=['universities', 'occupation', 'military', 'music', 'tv', 'personal'])      
        #query_array = api.users.search(q=query_string, count=1, fields=['universities', 'occupation', 'military', 'movies', 'music', 'tv', 'personal'])
        
        print(query_array)
        time.sleep(1)
        user_vector = []
        has_university = 0
        has_military = 0
        which_music = 0
        which_movies = ""
        which_occupation = 0
        how_many_followers = 0
        try:
            try:
                info = query_array[1]
                if 'universities' in info:
                    has_university = 1
                if 'military' in info:
                    if len(info['military']) > 0:
                        has_military = 1
                #if 'movies' in info:
                    #which_movies = info['movies']
                if 'occupation' in info:
                    if info['occupation']['type'] == 'work':
                        which_occupation = 1
                    elif info['occupation']['type'] == 'university':
                        which_occupation = 2
                    elif info['occupation']['type'] == 'school':
                        which_occupation = 3
                followers_array = api.users.getFollowers(user_id=info['uid'])
                how_many_followers = followers_array['count']          
                if 'music' in info:
                    blob = TextBlob(info['music'].lower(), classifier = cl)
                    print(blob)
                    music_answer = blob.classify()
                    print(blob.classify())
                    if music_answer == "classic":
                        which_music = 1
                    elif music_answer == "rock":
                        which_music = 2
                    elif music_answer == "ruspop":
                        which_music = 3
                    elif music_answer == "pop":
                        which_music = 4
                    print('music end')
            except KeyError:
                pass
            user_vector = [has_university, has_military, which_music, which_occupation, how_many_followers]
        except IndexError:
            user_vector = [has_university, has_military, which_music, which_occupation, how_many_followers]
        print('uservector: ')
        print(user_vector)
    return HttpResponseRedirect('/')
 
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