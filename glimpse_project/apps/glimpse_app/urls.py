from django.conf.urls import url
from . import views       
urlpatterns = [
    url(r'^$', views.index),
    url(r'^createUser$', views.createUser),
    url(r'^login$', views.login),
    url(r'^userPage$', views.userPage),
    url(r'^godModeCheck$', views.godModeCheck),
    url(r'^godMode$', views.godMode),
    url(r'^logout$', views.logout),
]  