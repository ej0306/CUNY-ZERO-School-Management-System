from django.urls import path
from . import views

app_name = 'courses'
urlpatterns = [
     path('search_result/', views.class_search_results, name='class_search_result'),
    path('', views.courses_offered, name='courses_offered'),
    path('description/', views.description, name='description'),
    
    # path('description/<int:course_id>/', views.description, name='description'),

]
