from django.shortcuts import render, redirect
from django.http import Http404
from courses.models import Course, Classes
from django.db.models import Q

# Create your views here.

# View for the courses offered page
def courses_offered(request):
    model = Course
    #Show all courses
    courses = Course.objects.order_by('title')
    context = {'courses' : courses}
    return render(request, 'courses/courses_offered.html', context)


# Handles the class search results

def class_search_results(request):        
    if request.method == 'GET': # this will be GET now      
        class_sem =  request.GET.get('class_search_results') # do some research what it does       
       
        status = Classes.objects.filter(semester__icontains='fall') # filter returns a list so you might consider skip except part
       
        return render(request,"class_search_result.html",{"Classes":status})
    else:
        return render(request,"class_search_result.html",{})

        
# def class_search_results(request):
#     model = Classes
    
#     def get_queryset(self): 
#         query = self.request.GET.get('q')
#         object_list = Classes.objects.filter(
#             Q(class_id__icontains='fall') | Q(semester__icontains='spring')
#             #| Q(instructor__icontains=query) | Q(course__icontains=query)
#         )
#         return object_list

#     return render(request, 'courses/class_search_result.html', {}) 
    

def description(request):
    return render(request, 'courses/course_description.html')


