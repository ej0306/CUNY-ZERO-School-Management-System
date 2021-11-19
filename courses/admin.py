from django.contrib import admin
from courses.models import Course, Classes

# Register your models here.
#class CityAdmin(admin.ModelAdmin):
    #list_display = ("name", "state",)

class CourseAdmin (admin.ModelAdmin):
    list_display = ("course_name" , "title",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Classes)


