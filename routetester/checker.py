import sys
import json
import collections
import copy
import logging
import functools

from .util import when
from .trip import Trip
from .tripmatcher import TripMatcher

def median(values):
    n = len(values)
    if n < 1:
        return None
    if n % 2 == 1:
        return sorted(values)[n//2]
    else:
        return sum(sorted(values)[n//2-1:n//2+1])/2.0

class ResponseSet(object):
    def __init__(self, responses=None):
        self.responses = responses or []
    
    def add_response(self, response):
        self.responses.append(response)

    def json(self):
        rs = self.responses
        passed = [i for i in rs if len(i.errors) == 0]
        failed = [i for i in rs if len(i.errors) != 0]
        response_times = [i.response_time for i in rs]
        eflat = set()
        for i in rs:
            for j in i.errors:
                eflat.add(str(j))
        return {
            'url': rs[0].url,
            'ok200': len([i for i in rs if i.status_code == 200]),
            'not200': len([i for i in rs if i.status_code != 200]),
            'passed': len(passed),
            'failed': len(failed),
            'response_time_min': min(response_times),
            'response_time_median': median(response_times),
            'response_time_max': max(response_times),
            'errors': "; ".join(sorted(eflat)),
            'responses': [i.json() for i in rs]
        }

class Checker(object):
    def __init__(self, host=None, request_cls=None, request_factories=None, when=None, whentz=None, params=None, count=1):
        self.host = host
        self.request_factories = request_factories or []
        if host and request_cls:
            self.request_factories.append(functools.partial(request_cls, host))
        self.rsets = collections.defaultdict(ResponseSet)
        self.queue = []
        self.count = count
        self.when = when
        self.whentz = whentz
        self.params = params

    def load(self, testfile):
        with open(testfile) as f:
            data = json.load(f)
        for feature in data.get('features',[]):
            feature['id'] = len(self.queue)
            if self.when:
                feature['properties']['when'] = self.when
            if self.whentz:
                feature['properties']['whentz'] = self.whentz
            trip = Trip(**feature)
            self.queue.append(trip)

    def run(self):
        for trip in self.queue:
            for f in self.request_factories:
                for _ in range(self.count):
                    request = f()
                    response = request.request(trip, params=self.params)
                    response.errors += TripMatcher().check(trip, response)
                    logging.info("%s -> %s"%(response.url, response.status_code))
                    self.rsets[trip].add_response(response)

    def result_geojson(self):
        features = []
        for trip, rset in self.rsets.items():
            stats = rset.json()
            passed = stats['passed']
            failed = stats['failed']
            trip = copy.copy(trip)
            # set display color
            style = {}
            status = 'unknown'
            color = '#cccccc'
            if passed and not failed:
                status = 'succeeded'
                color = '#00ff00'
            elif passed:
                status = 'mixed'
                color = '#ffff66'
            elif failed:
                status = 'failed'
                color = '#ff0000'
            style['status'] = status
            style['stroke'] = color
            style['stroke-width'] = 4
            style['stroke-opacity'] = 1.0
            # update
            trip.update(**style)
            trip.update(result=stats)
            features.append(trip.as_feature())
        return {
            "type": "FeatureCollection",
            "features": features
        }
