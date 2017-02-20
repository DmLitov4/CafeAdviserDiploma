from django.db import models
from django.utils import timezone

# Create your models here.
class Cities(models.Model):
	cityname = models.CharField(max_length=30)
	zipcode = models.IntegerField()
	created_date = models.DateTimeField(default=timezone.now)

def __str__(self):
	return self.cityname