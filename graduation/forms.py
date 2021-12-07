from django import forms
from django.forms import ModelForm, ModelChoiceField
from django.db import transaction
from .models import GraduatingClass, GraduationApplication


class GraduationApplicationForm(ModelForm):
    graduation_class = ModelChoiceField(queryset=GraduatingClass.objects.filter(session__is_current_session=True))

    class Meta:
        model = GraduationApplication
        fields = ['graduation_class']


class AcceptApplication(forms.Form):
    DECISION_CHOICES = (
        ('Y', 'Accept'),
        ('N', 'Reject'),
    )

    decision = forms.ChoiceField(required=True, widget=forms.RadioSelect, choices=DECISION_CHOICES)



