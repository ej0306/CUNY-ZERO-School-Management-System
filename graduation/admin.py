from django.contrib import admin
from .models import GraduatingClass, GraduationApplication

# Register your models here.
admin.site.register(GraduatingClass)
admin.site.register(GraduationApplication)