from django.urls import path
from . import views
from django.conf.urls import url

app_name = 'courses'

urlpatterns = [
    # path(r'^$', views.class_search, name='class_search'),
    path('search/', views.class_search, name='class_search'),
    path('register_course/', views.course_registration, name='course_registration'),
    path('course_drop/', views.course_drop, name='course_drop'),
    path('', views.courses_offered, name='courses_offered'),
    path('list_classes/', views.list_classes, name='list_classes'),
    path('course_allocation/', views.course_allocation_view, name='course_allocation_view'),
    path('add_score/', views.add_score, name='add_score'),
    path('add_score/<int:id>/', views.add_score_for, name='add_score_for'),
    path('view_result/', views.view_result, name='view_result'),


    path('description/', views.description, name='description'),
    
    # path('description/<int:course_id>/', views.description, name='description'),

]





# from django.shortcuts import render
# from django.db.models import Q
# from posts.models import Post

# def searchposts(request):
#     if request.method == 'GET':
#         query= request.GET.get('q')

#         submitbutton= request.GET.get('submit')

#         if query is not None:
#             lookups= Q(title__icontains=query) | Q(content__icontains=query)

#             results= Post.objects.filter(lookups).distinct()

#             context={'results': results,
#                      'submitbutton': submitbutton}

#             return render(request, 'search/search.html', context)

#         else:
#             return render(request, 'search/search.html')

#     else:
#         return render(request, 'search/search.html')
