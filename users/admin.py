from django.contrib import admin
from django.db import models
from .models import Reports, User, Student, Instructor, Registrar, EnrollmentApplication


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name",)

class ReportAdmin(admin.ModelAdmin):
    mmodel = Reports
    list_display = ('subject', 'description', 'owner', 'date_added')
    list_filter= ['date_added', 'owner']
    search_fields = ['description']

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Registrar)
admin.site.register(EnrollmentApplication)
admin.site.register(Reports, ReportAdmin)