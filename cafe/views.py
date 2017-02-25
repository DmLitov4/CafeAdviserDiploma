from django.shortcuts import render
from django.conf import settings
from decimal import Decimal
from .models import Cities
from .models import Cuisine
from .models import Kind
from .models import Cafe
from .models import Areaplace
from urllib.request import urlopen
import time
import xmltodict
import json
import codecs
from django_google_places.models import Place
from django_google_places.api import google_places
from googleplaces import GooglePlaces, types, lang

def load_cafes_from_google_api():
         if 1:
             return ''
         my_key = settings.GOOGLE_PLACES_API_KEY
         google_places = GooglePlaces(my_key)
         query_result = google_places.text_search(query="кафе и рестораны ростов-на-дону", radius=25000, language=lang.RUSSIAN, types=[types.TYPE_FOOD, types.TYPE_CAFE, types.TYPE_RESTAURANT])
         for place in query_result.places:
             place.get_details()
             if not Cafe.objects.filter(name=place.name).exists():
                 address_list = place.formatted_address.split(',')
                 city1=address_list[2].strip()
                 city2=address_list[1].strip()
                 response = urlopen('https://geocode-maps.yandex.ru/1.x/?geocode=' + place.formatted_address + '&format=json')
                 reader = codecs.getreader("utf-8")
                 data = json.load(reader(response))
                 print(data['response']['GeoObjectCollection']['featureMember'][0])
                 print(city1)
                 print(city1 == "Ростов-на-Дону")
                 if Cities.objects.filter(cityname=city1).exists():
                     city_type=Cities.objects.get(cityname=city1)
                 else:
                     city_type=Cities.objects.get(cityname=city2)
                 area_type=Areaplace.objects.get(areaplacename="Октябрьский район")
                 kind_type=Kind.objects.get(kindname="ресторан")
                 caf = Cafe(name=place.name, rating=place.rating, city=city_type, areaplace=area_type, kind=kind_type, bill=1, formatted_address=place.formatted_address)
                 caf.save()

def start_page(request):
    cafe_list = load_cafes_from_google_api()
    return render(request, 'cafe/start_page.html', {'cafe_list': cafe_list})