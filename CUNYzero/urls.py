"""CUNYzero URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('enrollment_applications/', user_views.enrollment_applications, name='enrollment_applications'),
    path('enrollment_applications/<int:pk>/', user_views.enrollment_application_details, name='application_details'),
    path('register_student/', user_views.register_student, name='register_student'),
    path('register_instructor/', user_views.register_instructor, name='register_instructor'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', user_views.LoginUser.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url(r'^password/$', user_views.change_password, name='change_password'),
    path('student_list/', user_views.student_list, name='student_list'),
    path('instructor_list/', user_views.instructor_list, name='instructor_list'),
    path('', include('general.urls')),
    path('courses/', include('courses.urls')),
]



