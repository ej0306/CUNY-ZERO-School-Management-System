from django.urls import path
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from general import views
from users import views as user_views
from django.conf.urls import url


urlpatterns = [
    path('', views.homepage, name='general-home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('registerInstructor/', views.registerinstructor, name='registerInstructor'),
    path('registerStudent/', views.registerStudent, name='registerStudent'),
    path('enrollment_applications/',views.enrollment_applications,name='enrollmentapplications'),
    path('profilebase/', views.profilebase, name='profilebase'),
    path('instructorlist/', views.instructor_list, name='instructorlist'),
    path('change_password/', views.change_password, name='instructorlist'),
    path('homelogin/', views.homelogin, name='homelogin'),
    path('instructorpage/', views.instructorpage, name='instructorpage'),
]

