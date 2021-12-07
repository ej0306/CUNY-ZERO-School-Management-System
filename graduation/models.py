from django.db import models
from courses.models import Session, Course, Classes, TakenCourse
from users.models import Student
from datetime import datetime


# Create your models here.
class GraduatingClass(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    graduation_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.session.__str__()

    # def check_graduation_requirements(self, student):
    #      student = Student.objects.get(user__pk=request.user.id)
    #      taken_courses = TakenCourse.objects.filter(student__user__id=request.user.id)


class GraduationApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    graduation_class = models.ForeignKey(GraduatingClass, on_delete=models.CASCADE)

    pending = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.student.__str__()

