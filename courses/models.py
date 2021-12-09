from datetime import MINYEAR
import datetime
from typing import Optional, Reversible
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import IntegerField
from django.utils import timezone, tree
import numpy as np
import datetime
import pytz
from users.models import Instructor, Student, User

# Create your models here.
A = "A"
B = "B"
C = "C"
D = "D"
F = "F"
W = "W"
PASS = "PASS"
FAIL = "FAIL"

GRADE = (
		(A, 'A'),
		(B, 'B'),
		(C, 'C'),
		(D, 'D'),
		(F, 'F'),
	)

COMMENT = (
		(PASS, "PASS"),
		(FAIL, "FAIL"),
	)

FIRST = "First"
SECOND = "Second"

SEMESTER = (
    (FIRST, "First"),
    (SECOND, "Second"),

)
M = "Mon"; T = "Tue"; W = "Wed"; Th = "Thu" ; Fr = "Fri" ; S = "Sat"; Su = "Sun"
MW = "Mon, Wed"; TT = "Tue, Thu"; MWT = "Mon, Wed, Thu"; TTF = "Tue, Thu, Fri" 
WF = "Wed, Fri"; SS = "Sat, Sun"

DAYS = (
    (M, "Mon"), (T, "Tue"), (W, "Wed"),(Th, "Thu"),
    (Fr, "Fri"), (S, "Sat"), (Su, "Sun"),
    (MW, "Mon, Wed"), (TT, "Tue, Thu"), (MWT, "Mon, Wed, Thu"),
    (TTF, "Tue, Thu, Fri"), (WF, "Wed, Fri"), (SS, "Sat, Sun")

)

CSU_PERIOD = "Class Set-Up Period"
CR_PERIOD = "Course Registration Period"
CLR_PERIOD = "Class Running Period"
GR_PERIOD = "Grading Period"


PERIODS = (
    (CSU_PERIOD , "Class Set-Up Period"),
    (CR_PERIOD , "Course Registration Period"),
    (CLR_PERIOD , "Class Running Period"),
    (GR_PERIOD , "Grading Period"),

)


# -----------------------------------------------------------------------------------------#
#                              Courses/Classes Related Models                             #
# -----------------------------------------------------------------------------------------#


# The courses models
class Course(models.Model):
    course_name = models.CharField(max_length = 20, null = True) 
    title = models.CharField(max_length = 100, null = True) 
    department = models.CharField(max_length = 100, null = True) 
    program = models.CharField(max_length = 50, null = True) 
    description = models.TextField(null= True)

    def __str__(self) -> str:
        return self.course_name + " -  " + self.title + " -  " + self.department


class Classes(models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    class_id = models.CharField( max_length= 10, null= True, unique=True)
    section_num = models.CharField(max_length= 20, null= True)
    credit = models.IntegerField(null = True)
    year = models.IntegerField( null= True)
    semester = models.CharField(choices= SEMESTER, max_length= 50, null=True)
    full_capacity = models.IntegerField(null= True)
    start_date = models.DateField(auto_now=False, null = True, auto_now_add=False, default= datetime.date(1, 1, 1))
    end_date = models.DateField(auto_now=False, null = True, auto_now_add=False, default= datetime.date(1, 1, 1))
    days = models.CharField(choices=DAYS, max_length= 50, null = True)
    start_time = models.TimeField(auto_now=False, auto_now_add=False, null= True)
    end_time = models.TimeField(auto_now=False, auto_now_add=False, null= True)
    instructor = models.ForeignKey(Instructor, on_delete= models.CASCADE, null= True)

    

    def get_cur_capacity(self):
        cur_capacity = TakenCourse.objects.filter(classes__class_id= self.class_id)
        return cur_capacity.count()


    def average_rating(self):
        all_ratings = map(lambda x: x.rate, self.reviewclasses_set.all())
        ar = np.mean(list(all_ratings)) # np -> numpy
        return ar

    def __str__(self):
        return self.course.course_name + " -  " + self.class_id + " -  " + self.course.title + " -  " + self.section_num

    class Meta:
        verbose_name_plural = 'classes'


class Session(models.Model):
    session = models.CharField(max_length=200, unique=True)
    is_current_session = models.BooleanField(default=False, blank=True, null=True)
    next_session_begins = models.DateField(blank=True, null=True)

    current_period = models.CharField(choices= PERIODS, max_length= 200,  null= True, blank= True)

    class_set_up_period_start = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1))
    class_set_up_period_end = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1, 23, 59, 59))

    course_registration_period_start = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1))
    course_registration_period_end = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1, 23, 59, 59))

    class_running_period_start = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1))
    class_running_period_end = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1, 23, 59, 59))

    grading_period_start = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1))
    grading_period_end = models.DateTimeField(default=datetime.datetime(datetime.date.today().year, 1, 1, 23, 59, 59))

    def __str__(self):
        return self.session

    def is_class_set_up_period(self):
        start = self.class_set_up_period_start.replace(tzinfo=pytz.UTC)
        end = self.class_set_up_period_end.replace(tzinfo=pytz.UTC)
        return start <= timezone.now() <= end

    def is_course_registration_period(self):
        start = self.course_registration_period_start.replace(tzinfo=pytz.UTC)
        end = self.course_registration_period_end.replace(tzinfo=pytz.UTC)
        return start <= timezone.now() <= end

    def is_class_running_period(self):
        start = self.class_running_period_start.replace(tzinfo=pytz.UTC)
        end = self.class_running_period_end.replace(tzinfo=pytz.UTC)
        return start <= timezone.now() <= end

    def is_grading_period(self):
        start = self.grading_period_start.replace(tzinfo=pytz.UTC)
        end = self.grading_period_end.replace(tzinfo=pytz.UTC)
        return start <= timezone.now() <= end


class CourseAllocation(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Classes, related_name='allocated_course')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.instructor.user.last_name


# <<<<<<< HEAD
# =======
class WaitList(models.Model):
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    course = models.ForeignKey(Classes, on_delete= models.CASCADE)
    instructor = models.ForeignKey(Instructor, null=True, blank= True, on_delete= models.CASCADE)

    # def __str__(self):
    #     return self.student.user.last_name +  " - " + self.course.class_id + " - " + self.instructor.user.last_name

#
# >>>>>>> origin/Last_Saves
class TakenCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classes = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='taken_courses')
    ca = models.PositiveIntegerField(blank=True, null=True, default=0)
    exam = models.PositiveIntegerField(blank=True, null=True, default=0)
    total = models.PositiveIntegerField(blank=True, null=True, default=0)
    grade = models.CharField(choices=GRADE, max_length=1, blank=True)
    comment = models.CharField(choices=COMMENT, max_length=200, blank=True)

    # def get_absolute_url(self):
    #     return Reversible('update_score', kwargs={'pk': self.pk})

    def get_student_count(self):
        student_count = self.student.count()
        return student_count


    def get_total(self, ca, exam):
        return int(ca) + int(exam)

    def get_grade(self, ca, exam):
        total = int(ca) + int(exam)
        if total >= 90:
            grade = A
        elif total >= 80:
            grade = B
        elif total >=70:
            grade = C
        elif total >=65:
            grade = D
        else:
            grade = F
        return grade

    def get_comment(self, grade):
        if not grade == "F":
            comment = PASS
        else:
            comment = FAIL
        return comment

    def carry_over(self, grade):
        if grade == F:
            CarryOverStudent.objects.get_or_create(student=self.student, course=self.classes)
        else:
            try:
                CarryOverStudent.objects.get(student=self.student, course=self.classes).delete()
            except:
                pass

    def is_repeating(self):
        count = CarryOverStudent.objects.filter(student__id=self.student.id)
        units = 0
        for i in count:
            units += int(i.classes.credit)
        if count.count() >= 6 or units >=16:
            RepeatingStudent.objects.get_or_create(student=self.student, level=self.student.semester)
        else:
            try:
                RepeatingStudent.objects.get(student=self.student, level=self.student.semester).delete()
            except:
                pass

    def calculate_gpa(self, total_unit_in_semester):
        current_session = Session.objects.get(is_current_session=True)
        student = TakenCourse.objects.filter(student=self.student, classes__semester=self.student.semester)
        p = 0
        point = 0
        for i in student:
            credit = i.classes.credit
            if i.grade == A:
                point = 5
            elif i.grade == B:
                point = 4
            elif i.grade == C:
                point = 3
            elif i.grade == D:
                point = 2
            else:
                point = 0
            p += int(credit) * point
        try:
            gpa = (p / total_unit_in_semester)
            return round(gpa, 1)
        except ZeroDivisionError:
            return 0
    
    def calculate_cgpa(self):
        current_session = Session.objects.get(is_current_session=True)
        current_semester = Student.objects.filter(student__semester = self.student.semester)
        previousResult = Result.objects.filter(student__id=self.student.id, level__lt=self.student.semester)
        previousCGPA = 0
        for i in previousResult:
            if i.cgpa is not None:
                previousCGPA += i.cgpa
        cgpa = 0
        if str(current_semester) == SECOND:
            try:
                first_sem_gpa = Result.objects.get(student=self.student.id, level=FIRST) 
                first_sem_gpa += first_sem_gpa.gpa.gpa
            except:
                first_sem_gpa = 0

            try:
                sec_sem_gpa = Result.objects.get(student=self.student.id, level=SECOND) 
                sec_sem_gpa += sec_sem_gpa.gpa
            except:
                sec_sem_gpa = 0

            taken_courses = TakenCourse.objects.filter(student=self.student, student__semester=self.student.semester)
            TCU = 0
            for i in taken_courses:
                TCU += int(i.classes.credit)
            cpga = first_sem_gpa + sec_sem_gpa / TCU
            
            return round(cgpa, 2)


    class Meta:
	    verbose_name_plural = 'TakenCourses'




class CarryOverStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Classes, on_delete=models.CASCADE)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(choices=SEMESTER, max_length=10, blank=True, null=True)

    def __str__(self):
        return self.student.id_number




class RepeatingStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    level = models.CharField(max_length=100, choices=SEMESTER)
    session = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.student.id_number



class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField(null=True)
    cgpa = models.FloatField(null=True)
    session = models.CharField(max_length=100, blank=True, null=True)
    level = models.CharField(max_length=100, choices=SEMESTER)

    def __str__(self):
        return self.student.id_number



#-----------------------------------------------------------------------------------------#
#                                   Reviews Models                                        #
#-----------------------------------------------------------------------------------------#

class ReviewClasses(models.Model):

    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    course = models.ForeignKey(Classes, on_delete= models.CASCADE)
    rate = models.IntegerField (choices = RATING_CHOICES, null=True)
    review = models.TextField(null=True)
    date_added = models.DateTimeField(auto_now_add= True)
    owner = models.ForeignKey(Student, on_delete= models.CASCADE)



    # def __str__(self) :
    #     return self.course.course.course_name + f"{ self.review[:50]}..."


class WarningCount(models.Model):
    student = models.ForeignKey(Student, on_delete= models.CASCADE)
    count = models.CharField(max_length=1,  null= True)


class AutomaticWarning(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    warning_text = models.TextField(null = True, blank= True)
    date_added = models.DateTimeField(auto_now_add= False, null= True)

