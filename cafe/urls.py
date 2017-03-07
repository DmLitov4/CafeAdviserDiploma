from django.conf.urls import url
from . import views
from login import views as l

urlpatterns = [
    url(r'^$', views.start_page, name='start_page'),
    url(r'^places/$', views.places, name='places'),
    url(r'^([_%&+0-9a-zA-Z ]+)/login/logout$', l.logout_page, name='logout'),
]