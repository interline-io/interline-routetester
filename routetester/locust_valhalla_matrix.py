import json
import random
from urllib.parse import urlencode
from locust import HttpLocust, TaskSet, task

class MatrixTaskSet(TaskSet):
    @task(1)
    def route(self):
        api_key = "REPLACE"
        num_locations = 50
        points = list(map(lambda _: { "lon": -random.randint(122349, 122522)/1000, "lat": random.randint(37694, 37814)/1000 }, list(range(num_locations))))
        json_dict = {
            "sources": points,
            "targets": points,
            "costing": "auto"
        }
        json_string = json.dumps(json_dict, separators=(',', ':'))
        # url = f"/sources_to_targets?api_key={api_key}&json={json_string}"
        url = f"/sources_to_targets?api_key={api_key}"
        print(f"POST {url} with {num_locations} sources and {num_locations} targets")
        response = self.client.post(url, verify=False, data=json_string, headers={'content-type': 'application/json'})
        print(response)

class TraceAttributesTest(HttpLocust):
    task_set = MatrixTaskSet
    min_wait = 5000
    max_wait = 9000
    host = "https://valhalla.interline.io"

# TO RUN: locust -f routetester/locust_valhalla_matrix.py