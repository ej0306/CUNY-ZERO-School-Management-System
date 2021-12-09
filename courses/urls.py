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
    path('first_class_list/', views.first_class_list, name='first_class_list'),
    path('repeating_list/', views.repeat_list, name='repeat_list'),
    path('add_class/', views.add_class, name='add_class'),
    path('add_course/', views.add_course, name='add_course'),
    path('wait_list/', views.wait_list_view, name='wait_list_view'),
    path('set_up_session/', views.set_up_session, name='set_up_session'),
    path('warning/', views.send_warnings_auto, name='send_warnings_auto'),

#-----------------------------------------------------------------------------------------#
#                            Reviews Classes URLs                                         #
#-----------------------------------------------------------------------------------------#
    path('course_list/', views.course_list, name='course_list'),
    path('course_list/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course_list/<int:course_id>/add_review/', views.add_review, name='add_review'),
    path('review_list/', views.review_list, name='review_list'),
    path('review_list/<int:review_id>/', views.review_detail, name='review_detail'),
    path('best_rated/', views.best_rated_classes, name='best_rated_classes'),





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
