import datetime
from django import forms
from django.db import transaction
from django.forms.widgets import Textarea, SelectDateWidget, DateTimeInput, DateInput
from courses.models import ReviewClasses, TakenCourse, Course, Classes, Session
from users.models import User, Instructor



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
    session = forms.ModelChoiceField(label="Session", queryset=Session.objects.all(), to_field_name="session", required=True)
    instructor = forms.ModelChoiceField(label="Instructor", queryset=Instructor.objects.filter(user__is_instructor=True, user__is_suspended=False), required=True)

    class Meta:
        model = Classes
        fields = ['course', 'section_num', 'session', 'credit', 'year', 'semester', 'full_capacity', 'start_date', 'end_date',
                  'days', 'start_time', 'end_time', 'instructor']
        widgets = {
            'start_date': SelectDateWidget(),
            'end_date': SelectDateWidget()
        }
        help_texts = {
            'start_time': 'HH:MM:SS'
        }


class CreateCourse(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'title', 'department', 'program', 'description']
        widgets = {
            'description': Textarea()
        }
        help_texts = {
            'course_name': "e.g., CSC 10100, ECO 10400",
            'title': "e.g., Software Engineering",
            'department': "e.g., Computer Science",
        }


class SetUpSession(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session', 'class_set_up_period_start', 'class_set_up_period_end',
                  'course_registration_period_start', 'course_registration_period_end',
                  'class_running_period_start', 'class_running_period_end',
                  'grading_period_start', 'grading_period_end',
                  'next_session_begins']
        widgets = {
            'class_set_up_period_start': DateTimeInput(),
            'class_set_up_period_end': DateTimeInput(),
            'course_registration_period_start': DateTimeInput(),
            'course_registration_period_end': DateTimeInput(),
            'class_running_period_start': DateTimeInput(),
            'class_running_period_end': DateTimeInput(),
            'grading_period_start': DateTimeInput(),
            'grading_period_end': DateTimeInput(),
            'next_session_begins': DateInput()
        }
        help_texts = {
            'session': "e.g., Fall 2021",
            'class_set_up_period_start': "YYYY-MM-DD HH:MM:SS",
            'class_set_up_period_end': "YYYY-MM-DD HH:MM:SS",
            'course_registration_period_start': "YYYY-MM-DD HH:MM:SS",
            'course_registration_period_end': "YYYY-MM-DD HH:MM:SS",
            'class_running_period_start': "YYYY-MM-DD HH:MM:SS",
            'class_running_period_end': "YYYY-MM-DD HH:MM:SS",
            'grading_period_start': "YYYY-MM-DD HH:MM:SS",
            'grading_period_end': "YYYY-MM-DD HH:MM:SS",
            'next_session_begins': "YYYY-MM-DD",
        }

