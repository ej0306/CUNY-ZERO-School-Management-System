import datetime
from django import forms
from django.db import transaction
from django.forms.widgets import Textarea

from courses.models import ReviewClasses, TakenCourse



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