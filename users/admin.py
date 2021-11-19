from django.contrib import admin
from django.db import models
from .models import User, Student, Instructor, Registrar

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name",)


admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Registrar)
