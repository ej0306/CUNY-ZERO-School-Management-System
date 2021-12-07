from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import scheduled_job_test
from courses.models import Session
import pytz
from multiprocessing import current_process


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_job_test, 'date', run_date=datetime(2021, 12, 6, 22, 44, 59))
    scheduler.start()

# replace run_date with this to schedule the task to be ran at the date stored in Session model:
# Session.objects.get(session='Spring 2022').class_set_up_period_start.replace(tzinfo=pytz.UTC)
