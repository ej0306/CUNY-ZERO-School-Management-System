from django.shortcuts import render
from django.http import HttpResponse
from . import views
from courses.models import Course, Result, ReviewClasses


# Create your views here.
def home(request):
    return render(request, 'general/home.html',{'title': 'Home'})

def registerinstructor(request):
    return render(request, 'registerInstructor.html',{'title': 'registerInstructor'})

def registerStudent(request):
    return render(request, 'registerStudent.html',{'title': 'registerStudent'})

def login(request):
    return render(request, 'login.html',{'title': 'login2'})