from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from general import views
from users import views as user_views
from django.conf.urls import url


urlpatterns = [
    path('', views.home, name='general-home'),
    path('login/', views.login, name='login'),
    path('registerInstructor/', views.registerinstructor, name='registerInstructor'),
    path('registerStudent/', views.registerStudent, name='registerStudent'),
]

