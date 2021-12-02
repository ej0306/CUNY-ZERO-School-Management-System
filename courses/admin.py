from django.contrib import admin
from courses.models import CarryOverStudent, Course, Classes, RepeatingStudent, Result, Session, TakenCourse, CourseAllocation

# Register your models here.
#class CityAdmin(admin.ModelAdmin):
    #list_display = ("name", "state",)

class CourseAdmin (admin.ModelAdmin):
    list_display = ("course_name" , "title",)

class CourseAllocationAdmin (admin.ModelAdmin):
    list_display = ("instructor" ,)

class ScoreAdmin(admin.ModelAdmin):
	list_display = ['student', 'classes', 'ca', 'exam', 'total', 'grade', 'comment']

class ClassesAdmin(admin.ModelAdmin):
	list_display = ['course', 'semester', 'start_date', 'end_date', 'instructor', 'days_and_time',]


admin.site.register(Course, CourseAdmin)
admin.site.register(Classes, ClassesAdmin)
admin.site.register(TakenCourse, ScoreAdmin)
admin.site.register(CourseAllocation, CourseAllocationAdmin)
admin.site.register(Session)
admin.site.register(Result)
admin.site.register(CarryOverStudent)
admin.site.register(RepeatingStudent)

