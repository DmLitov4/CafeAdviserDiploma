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
from .kmeans import *
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from celery.schedules import crontab
from celery.task import periodic_task
from datetime import timedelta

session = vk.Session(access_token=settings.VK_TOKEN)
api = vk.API(session)

def vk_clasterization():
    users = UserSettings.objects.all()
    vk_info_list = []
    print('selecting users...')
    with open('trainmusic.csv', 'r') as fp:
        cl = NaiveBayesClassifier(fp, format="csv")
    for u in users:
        query_string = u.user.first_name + ' ' + u.user.last_name
        print(query_string)
        query_array = api.users.search(q=query_string, city=119, age_from=u.age, age_to=u.age, count=1, fields=['universities', 'occupation', 'military', 'music'])      
        #query_array = api.users.search(q=query_string, count=1, fields=['universities', 'occupation', 'military', 'movies', 'music', 'tv', 'personal'])
        print(query_array)
        time.sleep(2)
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
                if 'occupation' in info:
                    if info['occupation']['type'] == 'work':
                        which_occupation = 1
                    elif info['occupation']['type'] == 'university':
                        which_occupation = 2
                    elif info['occupation']['type'] == 'school':
                        which_occupation = 3
                followers_array = api.users.getFollowers(user_id=info['uid'])
                if followers_array['count'] < 100:
                    how_many_followers = 0
                elif followers_array['count'] >= 100 and followers_array['count'] < 500:
                    how_many_followers = 1
                elif followers_array['count'] >= 500 and followers_array['count'] < 1000:
                    how_many_followers = 2
                elif followers_array['count'] >= 1000 and followers_array['count'] < 10000:
                    how_many_followers = 3
                elif followers_array['count'] >= 10000 and followers_array['count'] < 100000:
                    how_many_followers = 4
                elif followers_array['count'] >= 100000 and followers_array['count'] < 500000:
                    how_many_followers = 5
                elif followers_array['count'] >= 500000:
                    how_many_followers = 6
                if 'music' in info:
                    blob = TextBlob(info['music'].lower(), classifier = cl)
                    music_answer = blob.classify()
                    print(query_string)
                    print(music_answer)
                    if music_answer == "classic":
                        which_music = 1
                    elif music_answer == "rock":
                        which_music = 2
                    elif music_answer == "ruspop":
                        which_music = 3
                    elif music_answer == "pop":
                        which_music = 4
            except KeyError:
                pass
            user_vector = [has_university, has_military, which_music, which_occupation, how_many_followers]
        except IndexError:
            user_vector = [has_university, has_military, which_music, which_occupation, how_many_followers]
        print(user_vector)
        vk_info_list.append(user_vector)
    print(vk_info_list)
    return vk_info_list
 
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
            print("wrong!")
    else:
        form = RegistrationForm()
        update_vk_clasters()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )

def update_vk_clasters():
    vk_users_info = vk_clasterization()
    X = np.array(vk_users_info)
    kmeans = KMeans(n_clusters=5, random_state=None, max_iter=1000).fit(X)
    vk_user_clasters = kmeans.labels_
    print(vk_user_clasters)
    users = UserSettings.objects.all()
    step = 0
    for u in users:
        print('user')
        print(u)
        u.vkcategory = vk_user_clasters[step]
        step += 1
        u.save()
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

def login_page(request):
    try:
        remember = request.POST['remember_me']
        print(remember)
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
    print(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)
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