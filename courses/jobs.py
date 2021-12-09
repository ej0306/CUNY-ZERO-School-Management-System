# functions to be scheduled using APScheduler

from django.conf import settings
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from courses.models import *
from users.models import *
from warningsystem.models import *
import pytz


# perform course count checks at the end of registration period
def less_than_2_courses_check():
    stu = Student.objects.all()  # TO DO - do not include students with special registration

    for s in stu:
        taken_courses = TakenCourse.objects.filter(student__user_id=s.user_id)
        current_classes = taken_courses.filter(classes__session__is_current_session=True)
        if current_classes.count() < 2:
            Warnings.objects.create(user=s.user,
                                    description='Minimum Course Count Violation',
                                    details='Student failed to register in minimum 2 classes this semester.',
                                    issue_date=timezone.make_aware(datetime.datetime.now(),timezone.get_default_timezone()),
                                    registrar=Registrar.objects.all().first())
            print('Warning created - course count violation')
    print("job performed - course count check")


def cancel_low_student_count_classes():
    classes = Classes.objects.filter(session__is_current_session=True)

    for c in classes:
        if Student.objects.filter(takencourse__classes=c).count() < 5:
            c.cancelled = True
            c.save()
            # TO DO - de-register students in c and give them special registration
            Warnings.objects.create(user=c.instructor.user,
                                    description='Minimum Student Count Violation',
                                    details=c.course.__str__() + ' - Class did not meet minimum student count requirement (5) and has been cancelled.',
                                    issue_date=timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone()),
                                    registrar=Registrar.objects.all().first())
            print('Warning created - Student count violation - class cancelled')
            if classes.filter(cancelled=True, instructor=c.instructor).count() == classes.filter(instructor=c.instructor).count():
                c.instructor.user.is_suspended = True
                c.instructor.user.save()
                print('Instructor ' + c.instructor.user.__str__() + ' has been suspended')
    print("job performed - course count check")


# perform course count checks at the end of grading period
def low_rating_classes():
    pass


def missing_grades():
    pass


def extreme_class_gpa():
    pass


def low_gpa_students():
    pass


def failed_course_twice():
    pass


def honor_roll_students():
    pass

# Warnings.objects.filter(user=c.instructor.user, description='Minimum Student Count Violation').count() == 3
