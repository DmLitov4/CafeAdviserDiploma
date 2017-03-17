from django.db import models
from django.utils import timezone
from django_google_places.models import Place
from django_google_places.api import google_places
from django.core.validators import MaxValueValidator, MinValueValidator

class Cities(models.Model):
    cityname = models.CharField(max_length=30)
    zipcode = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return self.cityname

class Areaplace(models.Model):
    areaplacename = models.CharField(max_length=30)

    def __str__(self):
         return self.areaplacename

class Cuisine(models.Model):
    cuisinename = models.CharField(max_length=30)

    def __str__(self):
         return self.cuisinename

class Kind(models.Model):
	kindname = models.CharField(max_length=30)

	def __str__(self):
         return self.kindname

class Photo(models.Model):
    photourl = models.CharField(max_length=500)
    def __str__(self):
         return self.photourl

class Cafe(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey('Kind', on_delete=models.CASCADE)
    city = models.ForeignKey('Cities', on_delete=models.CASCADE, null=True)
    areaplace = models.ForeignKey('Areaplace', on_delete=models.CASCADE, null=True)
    cuisines = models.ManyToManyField(Cuisine, null=True, blank=True)
    bill = models.IntegerField(null=True)
    rating = models.FloatField(null=True)
    photos = models.ManyToManyField(Photo, blank=True)
    parking = models.NullBooleanField()
    formatted_address = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
         return self.name


