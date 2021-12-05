from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='general-home'),
    path('about/', views.about, name='general-about'),
    path('contact/', views.contact, name='contact'),
    path('loginbase/',views.loginbase, name='loginbase'),
    path('register/', views.base_page, name='register'),
    path('searchclasses/', views.base_page, name='searchclasses'),
    path('about/', views.about, name='about'),
    path('baseprofile/', views.base_profile, name='baseprofile'),
    path('basepage/', views.base_page, name='basepage'),
    path('login/', views.login,  name='login'),
]

