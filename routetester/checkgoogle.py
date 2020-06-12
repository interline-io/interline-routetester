import os
import sys
import json
import requests
import logging
import datetime
from dateutil import tz
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode, quote_plus

from .util import when, join
from .checker import Checker
from .request import Request
from .response import Response, Itinerary

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

@Request.register('google')
class GoogleRequest(Request):
    def url(self, trip, params=None):
        dt = trip.when()
        q = {
            'origin': join(trip.origin()[::-1]),
            'destination': join(trip.destination()[::-1]),
            'mode': 'transit',
            'departure_time': int(dt.timestamp()),
            'units': 'metric'
        }
        if params:
            q.update(params)
        url = "%s/maps/api/directions/json?%s"%(self.host, urlencode(q))
        return url

    def request(self, trip, params=None):
        url = self.url(trip, dict(params or {}, **{"key": API_KEY}))
        t = 0.0
        errors = []
        data = {}
        content = ''
        status_code = None
        try:
            req = requests.get(url)
            data = req.json()
            status_code = req.status_code
            t = req.elapsed.total_seconds()
        except requests.exceptions.RequestException as e:
            errors.append(e)
        return GoogleResponse(
            url=url,
            response=data, 
            status_code=status_code, 
            response_time=t,
            errors=errors
        )

class GoogleResponse(Response):
    def itins(self):
        itins = self.response.get('routes', [])
        return [GoogleItinerary(i) for i in itins]

class GoogleItinerary(Itinerary):
    def _legs(self):
        return self.data.get('legs', [])

    def _maneuvers(self):
        m = []
        for i in self._legs():
            for j in i.get('steps', []):
                m.append(j)
        return m

    def _walking_legs(self):
        return [i for i in self._maneuvers() if i['travel_mode'] == 'WALKING']

    def _transit_legs(self):
        return [i for i in self._maneuvers() if i['travel_mode'] == 'TRANSIT']

    def overall_duration(self):
        return sum(i['duration']['value'] for i in self._maneuvers())

    def overall_distance(self):
        return sum(i['distance']['value'] for i in self._maneuvers())

    def walking_distance(self):
        return sum(i['distance']['value'] for i in self._walking_legs())

    def routes(self):
        details = [i['transit_details'] for i in self._transit_legs()]
        return [i['line'].get('short_name') for i in details]

    def trips(self):
        # Not returned
        return []

    def stops(self):
        details = [i['transit_details'] for i in self._transit_legs()]
        stops = set()
        stops |= set([i['departure_stop']['name'] for i in details])
        stops |= set([i['arrival_stop']['name'] for i in details])
        return stops

    def agencies(self):
        details = [i['transit_details'] for i in self._transit_legs()]
        ret = set()
        for i in details:
            for j in i['line']['agencies']:
                ret.add(j['name'])
        return ret

    def duration_in_traffic(self):
        duration_in_traffic = 0.0
        for leg in self._legs():
            duration_in_traffic += leg.get("duration_in_traffic", {}).get("value", 0.0)
        return duration_in_traffic

