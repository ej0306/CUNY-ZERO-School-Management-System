from typing_extensions import Required
from django.shortcuts import render
from django.http import HttpResponse, response
# Create your views here.

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def register(request):
    return render(request, 'register.html')

def searchclasses(request):
    return render(request, 'searchclasses.html')

