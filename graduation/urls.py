from django.urls import path
from . import views


urlpatterns = [
    path('', views.apply_for_graduation, name='graduation_apply'),
    path('graduation_applications/', views.graduation_applications, name='grad_applications'),
    path('graduation_applications/<int:pk>/', views.graduation_application_details, name='grad_application_details'),
]
