import os
import sys
import json
import requests
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode, quote_plus
import logging

from .checker import Checker
from .request import Request
from .response import Response, Itinerary

API_KEY = os.getenv('VALHALLA_API_KEY')

@Request.register('valhalla')
class ValhallaRequest(Request):
    def url(self, trip, params=None):
        q = {
            "locations": [
                {"lon":trip.origin()[0], "lat":trip.origin()[1]},
                {"lon":trip.destination()[0], "lat":trip.destination()[1]}
            ],
            "costing": "pedestrian"
        }
        if params:
            q.update(params)
        url = '%s/route?%s'%(self.host, urlencode({'json':json.dumps(q, sort_keys=True, separators=(',', ':'))}))
        return url

    def request(self, trip, params=None):
        url = self.url(trip, params=params)
        urlsigned = "%s&api_key=%s"%(url, API_KEY)
        t = 0.0
        errors = []
        data = {}
        content = ''
        status_code = None
        try:
            req = requests.get(urlsigned)
            data = req.json()
            status_code = req.status_code
            t = req.elapsed.total_seconds()
        except requests.exceptions.RequestException as e:
            errors.append(e)
        logging.info("%s -> %s"%(url, status_code))
        return ValhallaResponse(
            url=url,
            response=data, 
            status_code=status_code, 
            response_time=t,
            errors=errors
        )

class ValhallaResponse(Response):
    def itins(self):
        trip = self.response.get('trip', {})
        if trip:
            return [ValhallaItinerary(trip)]
        return []

class ValhallaItinerary(Itinerary):
    def _legs(self):
        return self.data.get('legs', [])

    def _maneuvers(self):
        m = []
        for i in self._legs():
            for j in i.get('maneuvers', []):
                m.append(j)
        return m

    def _walking_legs(self):
        return [i for i in self._maneuvers() if i['travel_mode'] == 'pedestrian']

    def _transit_legs(self):
        return []

    def overall_duration(self):
        return sum(i['time'] for i in self._maneuvers())

    def overall_distance(self):
        return sum(i['length'] for i in self._maneuvers()) * 1000.0

    def walking_distance(self):
        return sum(i['length'] for i in self._walking_legs()) * 1000.0

    def routes(self):
        return [i['routeId'] for i in self._transit_legs()]

    def trips(self):
        return [i['tripId'] for i in self._transit_legs()]

    def stops(self):
        return [i['from']['stopId'] for i in self._transit_legs()]

    def agencies(self):
        return [i['agencyId'] for i in self._transit_legs()]

