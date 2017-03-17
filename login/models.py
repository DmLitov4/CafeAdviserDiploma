from django.db import models
from django.contrib.auth.models import User
from cafe.models import *

class UserSettings( models.Model ):

    user = models.ForeignKey(User)
    age = models.PositiveIntegerField(blank = True)
    city = models.CharField(max_length = 35, blank = True)
    MAN = 'М'
    WOMAN = 'Ж'
    GENDER_CHOICES = (
        (MAN, 'Мужской'),
        (WOMAN, 'Женский'),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default=MAN,
    )
    liked = models.ManyToManyField(Cafe, null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', blank = True)

    def __unicode__( self ) :
       return self.user.username