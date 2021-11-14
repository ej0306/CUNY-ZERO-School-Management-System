import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_registrar = models.BooleanField(default=False)

    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    m_initial = models.CharField(max_length=1, null=True)
    email = models.EmailField(max_length=254, default='')
    birth_date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date(1, 1, 1))
    phone_number = models.IntegerField(default=0)
    street_address = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=50, default='')
    state = models.CharField(max_length=2, default='')
    zip_code = models.IntegerField(default=0)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sc_name = models.CharField(max_length=50, null=True)
    sc_city = models.CharField(max_length=50, null=True)
    sc_state = models.CharField(max_length=2, null=True)
    graduation_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    gpa = models.FloatField(null=True)


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    resume = models.FileField(null=True)


class Registrar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
