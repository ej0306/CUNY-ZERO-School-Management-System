from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import *
import pytz


def start():
    scheduler = BackgroundScheduler()
    if Session.objects.filter(is_current_session=True).exists():
        scheduler.add_job(less_than_2_courses_check, 'date', run_date=Session.objects.get(is_current_session=True).course_registration_period_end.replace(tzinfo=pytz.UTC))
        scheduler.add_job(cancel_low_student_count_classes, 'date', run_date=Session.objects.get(is_current_session=True).course_registration_period_end.replace(tzinfo=pytz.UTC))
        scheduler.start()

