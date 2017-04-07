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
np.set_printoptions(threshold=np.nan, precision=4)
import time, xmltodict, json, codecs, re
from django_google_places.models import Place
from django_google_places.api import google_places
from googleplaces import GooglePlaces, types, lang
from .myutils import *
import vk, math

session = vk.Session(access_token=settings.VK_TOKEN)
api = vk.API(session)

search_radius = 35000
number_of_photos = 5
max_height = 1200
max_width = 1000

def load_cafes_from_google_api():
         if 1:
             return ''

         my_key = settings.GOOGLE_PLACES_API_KEY
         google_places = GooglePlaces(my_key)
         queries=['кафе ростов-на-дону', 'рестораны ростов-на-дону', 'бары ростов-на-дону', 'пабы ростов-на-дону', 'кондитерские ростов-на-дону', 'пиццерии ростов-на-дону']
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

def create_cafe_vectors(userrecords):
    statistic = []
    for record in userrecords:
        statistic_user = np.zeros(Cafe.objects.all().order_by("-id")[0].id + 1)
        statistic_user[0] = record.user_id
        for liked_cafe in record.liked.all():
            statistic_user[liked_cafe.id] = 1
        statistic.append(statistic_user)
    numpy_statistic = np.array(statistic)
    transposed_statistic = numpy_statistic.transpose()
    cafe_statistic = np.delete(transposed_statistic, (0), axis=0)
    k = 1
    final_statistic=[]
    for stat in cafe_statistic:
        try:
          if Cafe.objects.filter(id=k).exists():
              stat = np.insert(stat, 0, k)
          else:
              stat= np.insert(stat, 0, -1)
          final_statistic.append(stat)
        except:
          pass
        k += 1
    answer = np.array(final_statistic)
    final_answer = []
    for k in range(0, len(answer)-1):
        if (not answer[k][0] == -1.0) and (np.count_nonzero(answer[k]) > 1):
                final_answer.append(answer[k])
    answer = np.array(final_answer)
    np.savetxt("cafe_vectors.csv", answer.astype(int), fmt='%i', delimiter=",")
    return answer

def create_cafe_matrix():
    userrecords = UserSettings.objects.all()
    cafes = create_cafe_vectors(userrecords)
    cafe_ids = cafes[:,0]
    print(cafe_ids)
    num_of_cafes = len(cafes)
    cafe_matrix = np.zeros((num_of_cafes, num_of_cafes), np.float32)
    np.fill_diagonal(cafe_matrix, 0)
    for i in range(0, len(cafes)):
        for j in range(i + 1, len(cafes)):
            common = 0
            count_sum = 0
            for k in range(1, len(cafes[i])):
                if cafes[i][k] == cafes[j][k]:
                    common = common + 1
                count_sum = count_sum + math.pow(cafes[i][k] - cafes[j][k], 2)
            check = str(i) + " " + str(j) + " - " + str(common)
            tanimoto_coef = common / (len(cafes[i]) + len(cafes[j]) - common)
            euclid_coef = 1 - (math.sqrt(count_sum) / len(cafes[i]))
            res = str(i) + " " + str(j) + " - " + str(euclid_coef)
            cafe_matrix[i][j] = (tanimoto_coef + euclid_coef) / 2
    print(cafe_matrix)
    return (cafe_ids, cafe_matrix)

def collaborate_filtration():
    (cafe_ids, cafe_matrix) = create_cafe_matrix()
    
    return 1

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
            try:
                pricerange = request.POST.get('price')
                p = pricerange.split(",")
                minprice = p[0]
                maxprice = p[1]
            except:
                minpice = 0
                maxprice = 10000
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
