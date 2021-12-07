from django.shortcuts import render
from django.http import HttpResponse

from courses.models import Course, Result, ReviewClasses


# Create your views here.
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
