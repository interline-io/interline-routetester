import json
import random
from locust import HttpLocust, TaskSet, task

from .parse_gpx import *

class TraceAttributesTaskSet(TaskSet):
    @task(1)
    def route(self):
        random_filename = random.choice(list(self.locust.points_in_files))
        random_shape = self.locust.points_in_files[random_filename]
        req = {
            "shape": random_shape,
            "costing": "pedestrian",
            "directions_options": {"units": "miles"},
            "shape_match": "map_snap"
        }
        url = '/trace_attributes'
        print("POST ${url} with ${random_filename}")
        data = json.dumps(req, separators=(',', ':'))
        response = self.client.post(url, verify=False, data=data)
        print(response)


class TraceAttributesTest(HttpLocust):
    task_set = TraceAttributesTaskSet
    min_wait = 5000
    max_wait = 9000
    points_in_files = read_sample_gpx_files()
    host = "http://valhalla.interline.io"
