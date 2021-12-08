from django.db.models import Q
from django.forms import ModelForm, ModelChoiceField, Form
from .models import Warnings
from users.models import User


class IssueWarningForm(ModelForm):
    user = ModelChoiceField(queryset=User.objects.filter(Q(is_student=True) | Q(is_instructor=True)))

    class Meta:
        model = Warnings
        fields = ['user', 'description', 'details']

