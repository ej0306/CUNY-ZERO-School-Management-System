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
    return render(request, 'login.html',{'title': 'login'})

def logout(request):
    return render(request, 'logout.html',{'title': 'logout'})

def enrollment_applications(request):
    return render(request, 'enrollment_applications.html',{'title': 'enrollment_applications'})

def profilebase(request):
    return render(request, 'general/profilepage.html',{'title': 'profilepage'})

def instructor_list(request):
    return render(request, 'instructor_list.html',{'title': 'instructorlist'})

def change_password(request):
    return render(request, 'change_password.html',{'title': 'changepassword'})


def homepage(request):
    courses = Course.objects.all()
    students = Result.objects.filter(cgpa__gte=3.5)
    classes = ReviewClasses.objects.all()

    context = {
        'title': 'Home',
        "students": students,
        "classes": classes,
        "courses": courses,
    }
    return render(request, 'general/homepage.html',context)

def studentpage(request):
    return render (request,'general/studentpage.html',{'title': 'studentpage'})
