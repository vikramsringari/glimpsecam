from django.conf.urls import url
from . import views       
urlpatterns = [
    url(r'^$', views.index),
    url(r'^loginPage$', views.loginPage),
    url(r'^createUser$', views.createUser),
    url(r'^registerPage$', views.registerPage),
    url(r'^login$', views.login),
    url(r'^adminLogin$', views.adminLogin),
    url(r'^userPage$', views.userPage),
    url(r'^godModeCheck$', views.godModeCheck),
    url(r'^godMode$', views.godMode),
    url(r'^viewUserInfoGodMode/(?P<user_num>\d+)$', views.viewUserInfoGodMode),
    url(r'^viewImage/(?P<match>.+)/$', views.viewImage),
    url(r'^deleteUser/(?P<user_id>\d+)$', views.deleteUser),
    url(r'^logout$', views.logout)
]  