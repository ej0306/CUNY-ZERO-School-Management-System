# functions to be scheduled using APScheduler

from datetime import datetime
from django.conf import settings
import json
import random


def scheduled_job_test():
    n = random.randint(0, 100)

    print('Random Number: ' + str(n))
