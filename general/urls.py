from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='general-home'),
    path('about/', views.about, name='general-about'),
    path('home/', views.home2, name='home2'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('searchclasses/', views.searchclasses, name='searchclasses'),
    path('about/', views.about, name='about'),
    path('profile2/', views.profile2, name='profile2'),

]

