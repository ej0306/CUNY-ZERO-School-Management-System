from django.shortcuts import render
from django.http import HttpResponse

from courses.models import Course, Result, ReviewClasses


# Create your views here.
def home(request):
    return render(request, 'general/homepage.html',{'title': 'Home'})

def base_page(request):
    return render(request, 'general/base-page.html',{'title': 'Base Page'})

def contact(request):
    return render(request,'general/contact.html',{'title': 'Contact'})

def searchclasses(request):
    return render(request,'general/base-page.html',{'title': 'SearchClasses'})

def login(request):
    return render(request,'login.html',{'title': 'LogIn'})

def register(request):
    return render(request,'general/base-page.html',{'title': 'Register'})

def base_profile(request):
    return render(request,'general/base-profile.html',{'title': 'Profile'})

def about(request):
    return render(request, 'general/about.html',{'title': 'About'})
