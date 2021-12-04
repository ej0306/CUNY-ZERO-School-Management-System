from django.shortcuts import render
from django.http import HttpResponse

from courses.models import Course, Result, ReviewClasses


# Create your views here.
def home2(request):
    return render(request, 'general/homepage.html')

def contact(request):
    return render(request,'contact.html')

def about(request):
    return render(request,'about.html')

def searchclasses(request):
    return render(request,'searchclasses.html')

def login(request):
    return render(request,'login.html')

def register(request):
    return render(request,'register.html')

def profile2(request):
    return render(request,'general/profile2.html')

def home(request):
    courses = Course.objects.all()
    students = Result.objects.filter(cgpa__gte=3.5)
    classes = ReviewClasses.objects.all()

    context = {
        'title': 'Home',
        "students": students,
        "classes": classes,
        "courses": courses,
    }
    return render(request, 'general/home.html', context)


def about(request):
    return render(request, 'general/about.html', {'title': 'About'})
