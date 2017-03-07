from django.shortcuts import render
from django.conf import settings
from django.apps import AppConfig
from decimal import Decimal
from .models import Cities, Cuisine, Kind, Cafe, Areaplace, Photo
from decimal import Decimal
from urllib.request import urlopen
from django.contrib.auth.decorators import login_required
from itertools import islice
import login
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
         queries=['subway ростов']
         for q in queries:
             query_result = google_places.text_search(query=q, radius=25000, language=lang.RUSSIAN, types=[types.TYPE_FOOD, types.TYPE_CAFE, types.TYPE_RESTAURANT])
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

                         kind_type=Kind.objects.get(kindname="ресторан")
                         caf = Cafe(name=place.name, rating=place.rating, city=city_type, areaplace=area_type, kind=kind_type, bill=1, formatted_address=place.formatted_address)
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
                                 print(p.url)
                         except IndexError:
                             pass
                         
                     except UnicodeEncodeError:
                         pass

def get_cafe_list():
    return Cafe.objects.order_by('rating').reverse()[:12]

def get_latest_list():
    return Cafe.objects.order_by('created_date').reverse()[:4]

def start_page(request):
    cafe_list = load_cafes_from_google_api()
    latest_list = get_latest_list()
    return render(request, 'cafe/start_page.html', {'cafe_list': cafe_list, 'latest_list': latest_list})

@login_required(login_url='/')
def places(request):
    all_cafes = get_cafe_list()
    return render(request, 'cafe/places.html', {'all_cafes': all_cafes})
