from datetime import MINYEAR
from django.db import models
from django.db.models.deletion import CASCADE

from users.models import Instructor

# Create your models here.

# The courses models
class Course(models.Model):
    course_name = models.CharField(max_length = 20, null = True) 
    title = models.CharField(max_length = 100, null = True) 
    department = models.CharField(max_length = 100, null = True) 
    program = models.CharField(max_length = 50, null = True) 
    description = models.TextField(null= True)

    def __str__(self) -> str:
        return self.title

class Classes(models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    class_id = models.CharField( max_length= 10, null= True)
    section_num = models.CharField(max_length= 20, null= True)
    year = models.IntegerField( null= True)
    semester = models.CharField(max_length= 20, null= True)
    instructor = models.ForeignKey(Instructor, on_delete= models.CASCADE, null= True)

    def __str__(self) -> str:
        return self.course.course_name + " -  " + self.class_id + " -  " + self.course.title + " -  " + self.section_num

    class Meta:
	    verbose_name_plural = 'classes'