import datetime
from django import forms
from django.db import transaction
from django.forms.widgets import Textarea, SelectDateWidget, TimeInput

from courses.models import ReviewClasses, TakenCourse, Course, Classes



class CourseRegistration(forms.ModelForm):
    class Meta:
        model = TakenCourse
        fields = ('classes',)
        widgets = {
            'classes' : forms.CheckboxSelectMultiple
        }
    


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewClasses
        fields = ['rate', 'review']
        widgets = {
            'review': Textarea(attrs={'cols': 40, 'rows': 15})
        }


class ClassSetUp(forms.ModelForm):
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.all(), to_field_name="course_name", required=True)

    class Meta:
        model = Classes
        fields = ['course', 'section_num', 'credit', 'year', 'semester', 'full_capacity', 'start_date', 'end_date',
                  'days_and_time', 'instructor']
        widgets = {
            'start_date': SelectDateWidget(),
            'end_date': SelectDateWidget()
        }


class CreateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'title', 'department', 'program', 'description']
        widgets = {
            'description': Textarea()
        }
