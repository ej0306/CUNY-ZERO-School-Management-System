import datetime
from django import forms
from django.db import transaction

from courses.models import TakenCourse



class CourseRegistration(forms.ModelForm):
    class Meta:
        model = TakenCourse
        fields = ('classes',)
        widgets = {
            'classes' : forms.CheckboxSelectMultiple
        }
    