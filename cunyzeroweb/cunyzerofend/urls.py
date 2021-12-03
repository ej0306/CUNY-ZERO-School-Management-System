from django.urls import path
from . import views
from . views import home,contact,register,login,profile,searchclasses

urlpatterns=[
    path('contact/',views.contact, name='contact'),
    path('about/',views.about, name='about'),
    path('home/', views.home, name='home'),
    path('register/',views.register, name='register'),
    path('profile/',views.profile, name='profile'),
    path('searchclasses/',views.searchclasses, name='searchclasses'),
    path('login/',views.login, name='login')
]
