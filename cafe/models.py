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

class Area(models.Model):
    areaname = models.CharField(max_length=30)
    
    def __str__(self):
         return self.areaname

class Cuisine(models.Model):
    cuisinename = models.CharField(max_length=30)

    def __str__(self):
         return self.cuisinename

class Kind(models.Model):
	kindname = models.CharField(max_length=30)

	def __str__(self):
         return self.kindname

class Cafe(models.Model):
    name = models.CharField(max_length=35)
    kind = models.ForeignKey('Kind', on_delete=models.CASCADE)
    cuisines = models.ManyToManyField(Cuisine)
    rating = models.FloatField(validators = [MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
         return self.name


