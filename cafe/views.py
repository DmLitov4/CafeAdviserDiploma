from django.shortcuts import render
from django.conf import settings
from .models import Cities
from .models import Area
from .models import Cuisine
from .models import Kind
from .models import Cafe
import time
from django_google_places.models import Place
from django_google_places.api import google_places
from googleplaces import GooglePlaces, types, lang

def load_from_google_api2():
         if 1:
             return ''
         YOUR_API_KEY = settings.GOOGLE_PLACES_API_KEY
         google_places = GooglePlaces(YOUR_API_KEY)
         query_result = google_places.text_search(query='кафе+в+ростове')
         if query_result.has_attributions:
             print(query_result.html_attributions)
         for place in query_result.places:
             print(place.name)
             place.get_details()
             return place.website

def start_page(request):
    cafe_list = load_from_google_api2()
    return render(request, 'cafe/start_page.html', {'cafe_list': cafe_list})