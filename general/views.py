from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'general/home.html', context)


def about(request):
    return render(request, 'general/about.html', {'title': 'About'})
