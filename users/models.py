import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
FIRST = "First"
SECOND = "Second"

SEMESTER = (
    (FIRST, "First"),
    (SECOND, "Second"),
)

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
    id_number = models.CharField(max_length= 20, unique = True, null= True)
    sc_name = models.CharField(max_length=50, null=True)
    sc_city = models.CharField(max_length=50, null=True)
    sc_state = models.CharField(max_length=2, null=True)
    semester = models.CharField(choices= SEMESTER, max_length= 50, null=True)
    graduation_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    gpa = models.FloatField(null=True)

    def __str__(self) -> str:
        return self.user.last_name + ", " + self.user.first_name


    

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    resume = models.FileField(null=True)

    def __str__(self) -> str:
        return self.user.last_name + " " + self.user.first_name



class Registrar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self) -> str:
        return self.user.last_name + ", " + self.user.first_name
