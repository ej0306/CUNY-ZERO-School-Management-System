from django.urls import path
from . import views


urlpatterns = [
    path('issue_warning/', views.issue_warning, name='issue_warning'),
    path('issued_warnings_list/', views.issued_warnings_list, name='warnings_list'),
    path('issued_warnings_list/<int:pk>/', views.issued_warning_details, name='warning_details'),
    path('remove_warning/<int:pk>/', views.RemoveWarning.as_view(), name='remove_warning'),
]