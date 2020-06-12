import sys
import os
import random
import json

from locust import HttpLocust, TaskSet, task

from routetester.checker import Checker
from routetester.checkotp import OTPRequest

LOCUST_TESTFILE = os.getenv('LOCUST_TESTFILE')

def load_trips():
    # Load trips - specify adapter manually below
    if not LOCUST_TESTFILE:
        print('Must provide --testfile or LOCUST_TESTFILE env var')
        sys.exit(1)
    checker = Checker(None, None)
    checker.load(LOCUST_TESTFILE)
    return list(checker.queue)

class UserBehavior(TaskSet):
    @task(1)
    def route(self):
        trip = random.sample(self.locust.trips, 1)[0]
        url = OTPRequest(host=self.locust.host).url(trip)
        self.client.get(url)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 1000
    max_wait = 5000
    trips = load_trips()
