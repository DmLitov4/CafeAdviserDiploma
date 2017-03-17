from django.shortcuts import render
from django.conf import settings
from django.apps import AppConfig
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cafe.forms import *
from login.models import *
from .models import Cities, Cuisine, Kind, Cafe, Areaplace, Photo
from decimal import Decimal
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from itertools import islice
import login
import functools as ft
import numpy as np
import time, xmltodict, json, codecs, re
from django_google_places.models import Place
from django_google_places.api import google_places
from googleplaces import GooglePlaces, types, lang

def transliterate(string):

    capital_letters = {u'А': u'A',
                       u'Б': u'B',
                       u'В': u'V',
                       u'Г': u'G',
                       u'Д': u'D',
                       u'Е': u'E',
                       u'Ё': u'E',
                       u'З': u'Z',
                       u'И': u'I',
                       u'Й': u'Y',
                       u'К': u'K',
                       u'Л': u'L',
                       u'М': u'M',
                       u'Н': u'N',
                       u'О': u'O',
                       u'П': u'P',
                       u'Р': u'R',
                       u'С': u'S',
                       u'Т': u'T',
                       u'У': u'U',
                       u'Ф': u'F',
                       u'Х': u'H',
                       u'Ъ': u'',
                       u'Ы': u'Y',
                       u'Ь': u'',
                       u'Э': u'E',}

    capital_letters_transliterated_to_multiple_letters = {u'Ж': u'Zh',
                                                          u'Ц': u'Ts',
                                                          u'Ч': u'Ch',
                                                          u'Ш': u'Sh',
                                                          u'Щ': u'Sch',
                                                          u'Ю': u'Yu',
                                                          u'Я': u'Ya',}


    lower_case_letters = {u'а': u'a',
                       u'б': u'b',
                       u'в': u'v',
                       u'г': u'g',
                       u'д': u'd',
                       u'е': u'e',
                       u'ё': u'e',
                       u'ж': u'zh',
                       u'з': u'z',
                       u'и': u'i',
                       u'й': u'y',
                       u'к': u'k',
                       u'л': u'l',
                       u'м': u'm',
                       u'н': u'n',
                       u'о': u'o',
                       u'п': u'p',
                       u'р': u'r',
                       u'с': u's',
                       u'т': u't',
                       u'у': u'u',
                       u'ф': u'f',
                       u'х': u'h',
                       u'ц': u'ts',
                       u'ч': u'ch',
                       u'ш': u'sh',
                       u'щ': u'sch',
                       u'ъ': u'',
                       u'ы': u'y',
                       u'ь': u'',
                       u'э': u'e',
                       u'ю': u'yu',
                       u'я': u'ya',}

    capital_and_lower_case_letter_pairs = {}

    for capital_letter, capital_letter_translit in capital_letters_transliterated_to_multiple_letters.items():
        for lowercase_letter, lowercase_letter_translit in lower_case_letters.items():
            capital_and_lower_case_letter_pairs[u"%s%s" % (capital_letter, lowercase_letter)] = u"%s%s" % (capital_letter_translit, lowercase_letter_translit)

    for dictionary in (capital_and_lower_case_letter_pairs, capital_letters, lower_case_letters):

        for cyrillic_string, latin_string in dictionary.items():
            string = string.replace(cyrillic_string, latin_string)

    for cyrillic_string, latin_string in capital_letters_transliterated_to_multiple_letters.items():
        string = string.replace(cyrillic_string, latin_string.upper())

    return string


def load_cafes_from_google_api():
         if 1:
             return ''
         my_key = settings.GOOGLE_PLACES_API_KEY
         google_places = GooglePlaces(my_key)
         queries=['кафе батайск']
         for q in queries:
              try:
                 query_result = google_places.text_search(query=q, radius=39000, language=lang.RUSSIAN, types=[types.TYPE_FOOD, types.TYPE_CAFE, types.TYPE_RESTAURANT])
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
                                 iterator = islice(place.photos, 5)
                                 for p in iterator:
                                     p.get(maxheight=1200, maxwidth=1000)
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

kind_weight = 37
price_weight = 30
area_weight = 15
cuisine_weight = 15
parking_weight = 5

def common_elements(list1, list2):
    return list(set(list1) & set(list2))

def get_cafe(cafe_id):
    return Cafe.objects.get(id=cafe_id)

def get_cafe_list():
    return Cafe.objects.order_by('rating').reverse()

def get_latest_list():
    return Cafe.objects.order_by('created_date').reverse()[:4]

def get_cities_list():
    return Cities.objects.all()

def get_cuisines_list():
    return Cuisine.objects.all()

def get_areas_list():
    return Areaplace.objects.all()

def get_kinds_list():
    return Kind.objects.all()

def start_page(request):
    cafe_list = load_cafes_from_google_api()
    latest_list = get_latest_list()
    return render(request, 'cafe/start_page.html', {'cafe_list': cafe_list, 'latest_list': latest_list})

def count_weight(cuisines, areas, kinds, parking, minbill, maxbill, cafe):
    current_cuisines = cafe.cuisines.values_list('id', flat=True)
    cuisines = list(map(int, cuisines))
    cuisineweight = len(common_elements(cuisines, current_cuisines)) * cuisine_weight
    print(len(common_elements(cuisines, current_cuisines)))
    current_area = cafe.areaplace_id
    if current_area in areas:
        areaweight = area_weight
    else:
        areaweight = 0
    
    current_kind = cafe.kind_id
    if current_kind in kinds:
        kindweight = kind_weight
    else:
        kindweight = 0

    if cafe.bill > int(minbill) and cafe.bill < int(maxbill):
        priceweight = price_weight
    else:
        priceweight = 0

    return cuisineweight + areaweight + kindweight + priceweight

def context_filtration(city, cuisines, areas, kinds, parking, minbill, maxbill):
    cafe_list = Cafe.objects.filter(city=city)
    selected_list = list(reversed(sorted(ft.reduce(lambda acc, x: acc + [(x, count_weight(cuisines, areas, kinds, parking, minbill, maxbill, x))], cafe_list, []), key=lambda x: x[1])))
    return selected_list


@login_required(login_url='/')
def places(request):
    all_cities = get_cities_list()
    all_areas = get_areas_list()
    all_cuisines = get_cuisines_list()
    all_kinds = get_kinds_list()
    
    #userrecord = UserSettings.objects.filter(user_id=request.user.id)[0]
    if request.method == 'POST':
        if request.POST.get("liked"):
            print('liked liked liked')
            try:
                userrecord = UserSettings.objects.get(user_id = request.user.id)
                liked_cafe = Cafe.objects.get(id=request.POST.get('cafeid'))
                if not userrecord.liked_set.filter(cafe_id=liked_cafe).exists():
                    userrecord.liked.add(liked_cafe)
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
    print(np.eye(5))
    return render(request, 'cafe/place_details.html', {'cafe': cafe})
