from django.conf.urls import url
from . import views       
urlpatterns = [
    url(r'^$', views.index),
    url(r'^eventpage$', views.eventpage),
    url(r'^godMode$', views.godMode)
]  