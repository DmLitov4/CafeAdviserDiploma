from django.shortcuts import render
from django.conf import settings
from django.apps import AppConfig
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cafe.forms import *
import login
from login.models import *
from .models import Cities, Cuisine, Kind, Cafe, Areaplace, Photo
from decimal import Decimal
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from itertools import islice
import functools as ft
import numpy as np
import time, xmltodict, json, codecs, re
from django_google_places.models import Place
from django_google_places.api import google_places
from googleplaces import GooglePlaces, types, lang
from .myutils import *

search_radius = 35000
number_of_photos = 5
max_height = 1200
max_width = 1000

kind_weight = 37
price_weight = 30
area_weight = 15
cuisine_weight = 15
parking_weight = 5

def load_cafes_from_google_api():
         if 1:
             return ''

         my_key = settings.GOOGLE_PLACES_API_KEY
         google_places = GooglePlaces(my_key)
         queries=['кафе ростов-на-дону', 'рестораны ростов-на-дону', 'бары ростов-на-дону', 'пабы ростов-на-дону']
         for q in queries:
              try:
                 query_result = google_places.text_search(query=q, radius=search_radius, language=lang.RUSSIAN, types=[types.TYPE_FOOD, types.TYPE_CAFE, types.TYPE_RESTAURANT])
                 for place in query_result.places:
                     place.get_details()
                     if not Cafe.objects.filter(name=place.name).exists():
                         try:
                             address_list = place.formatted_address.split(',')
                             city1=address_list[2].strip()
                             city2=address_list[1].strip()
                             city3=address_list[3].strip()
                             response = urlopen(u"https://geocode-maps.yandex.ru/1.x/?geocode=" + transliterate(place.formatted_address) + u'&format=json')
                             reader = codecs.getreader("utf-8")
                             data = json.load(reader(response))
                             geolocation = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
                             reverse_response = urlopen(u"https://geocode-maps.yandex.ru/1.x/?geocode="+ geolocation + u'&format=json&kind=district')
                             district_dict = json.load(reader(reverse_response))
                             try:
                                 district = district_dict['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
                             except IndexError:
                                 continue
                             print(district)
                             if Cities.objects.filter(cityname=city1).exists():
                                 city_type=Cities.objects.get(cityname=city1)
                             elif Cities.objects.filter(cityname=city2).exists():
                                 city_type=Cities.objects.get(cityname=city2)
                             else:
                                 city_type=Cities.objects.get(cityname=city3)

                             if Areaplace.objects.filter(areaplacename=district).exists():
                                 area_type=Areaplace.objects.get(areaplacename=district)
                             else:
                                 area_type=Areaplace.objects.create(areaplacename=district)
                                 area_type.save()
                             kind_type=Kind.objects.get(kindname="бар")
                             caf = Cafe(name=place.name, rating=place.rating, city=city_type, areaplace=area_type, kind=kind_type, bill=1, website=place.website, formatted_address=place.formatted_address)
                             caf.save()
                             try:
                                 iterator = islice(place.photos, number_of_photos)
                                 for p in iterator:
                                     p.get(maxheight=max_height, maxwidth=max_width)
                                     if Photo.objects.filter(photourl=p.url).exists():
                                         ph = Photo.objects.get(photourl=p.url)
                                     else:
                                         ph = Photo.objects.create(photourl=p.url)
                                         ph.save()
                                     caf.photos.add(ph)
                             except IndexError:
                                 pass
                         
                         except UnicodeEncodeError:
                             pass
              except:
                  pass

def start_page(request):
    cafe_list = load_cafes_from_google_api()
    latest_list = get_latest_list()
    return render(request, 'cafe/start_page.html', {'cafe_list': cafe_list, 'latest_list': latest_list})

def context_filtration(city, cuisines, areas, kinds, parking, minbill, maxbill):
    cafe_list = Cafe.objects.filter(city=city)
    selected_list = list(reversed(sorted(ft.reduce(lambda acc, x: acc + [(x, count_weight(cuisines, areas, kinds, parking, minbill, maxbill, x))], cafe_list, []), key=lambda x: x[1])))
    return selected_list

def collaborate_filtration():
    userrecords = UserSettings.objects.all()
    statistic = []
    #cafe_ids = np.empty
    #for cafe in Cafe.objects.all():
    #    cafe_ids = np.append(cafe_ids, cafe.id)
    #statistic.append(cafe_ids)
    #print(statistic)
    for record in userrecords:
        statistic_user = np.zeros(len(Cafe.objects.all()) + 30)
        statistic_user[0] = record.user_id
        for liked_cafe in record.liked.all():
            print(str(liked_cafe.id) + ' ' + str(record.user_id))
            statistic_user[liked_cafe.id] = 1
        statistic.append(statistic_user)
    statistic2 = np.array(statistic)
    print(statistic2)
    print('****************')
    cafe_statistic = np.delete(statistic2.transpose(), (0), axis=0)
    #cafe_statistic = np.delete(statistic2.transpose(), (0), axis=0)
    cafs = Cafe.objects.all()
    k = 1
    print('длина кафе')
    print(len(cafe_statistic))

    #for row in cafe_statistic:
    #  try:
    #    row = np.append(cafs[k].id, row)
    #    print(row)
    #    k = k + 1
    #  except:
    #    pass
    #cafe_statistic = np.delete(cafe_statistic, 0, 0)  # delete second row of A
    print(cafe_statistic)
    #cafe_statistic.savefile
    

@login_required(login_url='/')
def places(request):
    collaborate_filtration()
    all_cities = get_cities_list()
    all_areas = get_areas_list()
    all_cuisines = get_cuisines_list()
    all_kinds = get_kinds_list()
    
    #userrecord = UserSettings.objects.filter(user_id=request.user.id)[0]
    if request.method == 'POST':
        if request.POST.get("liked"):
            print('liked')
            try:
                userrecord = UserSettings.objects.get(user_id = request.user.id)
                print('got userrecord')
                liked_cafe = Cafe.objects.get(id=request.POST.get('cafeid'))
                print('got likedcafe')
                if not liked_cafe in userrecord.liked.all():
                    userrecord.liked.add(liked_cafe)
                print('add liked now')
            except:
                print('does not exist')
                pass
        else:
            print(request.POST.get('liked' in request.POST))
        form = CriteriaForm(request.POST)
        if form.is_valid():
            city = request.POST.get('city')
            cuisines = request.POST.getlist('cuisine')
            areas = request.POST.getlist('area')
            kinds = request.POST.getlist('kind')
            parking = request.POST.get('parking')
            pricerange = request.POST.get('price')
            p = pricerange.split(",")
            minprice = p[0]
            maxprice = p[1]
            selected_list = context_filtration(city, cuisines, areas, kinds, parking, minprice, maxprice)
            all_cafes = [x[0] for x in selected_list]
            paginator = Paginator(all_cafes, 12)
            page = request.GET.get('page')
            try:
                all_cafes = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                all_cafes = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                all_cafes = paginator.page(paginator.num_pages)
            #all_cafes = Cafe.objects.filter(city=city)
            return render(request, 'cafe/places.html', {'form': form, 'all_cafes': all_cafes})
        else:
            all_cafes = get_cafe_list()
            paginator = Paginator(all_cafes, 12)
            page = request.GET.get('page')
            try:
                all_cafes = paginator.page(page)
            except PageNotAnInteger:
            # If page is not an integer, deliver first page.
                all_cafes = paginator.page(1)
            except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
                all_cafes = paginator.page(paginator.num_pages)
            return render(request, 'cafe/places.html', {'form': form, 'all_cafes': all_cafes})
    else:
        form = CriteriaForm()
        all_cafes = get_cafe_list()
        paginator = Paginator(all_cafes, 12)
        page = request.GET.get('page')
        try:
            all_cafes = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            all_cafes = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            all_cafes = paginator.page(paginator.num_pages)
        return render(request, 'cafe/places.html', {'form': form, 'all_cafes': all_cafes, 'all_cities': all_cities, 'all_areas': all_areas, 'all_cuisines': all_cuisines, 'all_kinds': all_kinds})

def place_details(request, cafe_id):
    cafe = get_cafe(cafe_id)
    return render(request, 'cafe/place_details.html', {'cafe': cafe})
