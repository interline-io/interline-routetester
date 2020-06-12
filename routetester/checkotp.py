import sys
import json
import requests
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode, quote_plus
import logging

from .util import when, join
from .checker import Checker
from .request import Request
from .response import Response, Itinerary

@Request.register('otp')
class OTPRequest(Request):
    def url(self, trip, params=None):
        dt = trip.when()
        # default request parameters
        q = {
            'fromPlace': join(trip.origin()[::-1]),
            'toPlace': join(trip.destination()[::-1]),
            'mode': 'TRANSIT,WALK',
            'maxWalkDistance': 800,
            'arriveBy': False,
            'wheelchair': False,
            'date': dt.strftime("%m-%d-%Y"), # OTP accepts both yyyy-mm-dd but prefers mm-dd-yyyy
            'time': dt.strftime("%H:%M:%S")
        }
        if params:
            q.update(params)
        url = "%s/otp/routers/default/plan?%s"%(self.host, urlencode(q))
        return url

    def request(self, trip, params=None):
        url = self.url(trip, params=params)
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
        if data.get("error"):
            errors.append(data.get("error", {}).get("msg"))        
        return OTPResponse(
            url=url,
            response=data, 
            status_code=status_code, 
            response_time=t,
            errors=errors
        )

class OTPResponse(Response):
    def itins(self):
        itins = self.response.get('plan', {}).get('itineraries', [])
        return [OTPItinerary(i) for i in itins]

class OTPItinerary(Itinerary):
    def _legs(self):
        return self.data.get('legs', [])

    def _walking_legs(self):
        return [i for i in self._legs() if i['mode'] == 'WALK']

    def _transit_legs(self):
        return [i for i in self._legs() if i['transitLeg']]

    def overall_duration(self):
        return sum(i['duration'] for i in self._legs())

    def overall_distance(self):
        return sum(i['distance'] for i in self._legs())

    def walking_distance(self):
        return sum(i['distance'] for i in self._walking_legs())

    def routes(self):
        return [i.get('routeShortName') for i in self._transit_legs()]

    def trips(self):
        return [i['tripId'] for i in self._transit_legs()]

    def stops(self):
        stops = set()
        stops |= set([i['from']['name'] for i in self._transit_legs()])
        stops |= set([i['to']['name'] for i in self._transit_legs()])
        return stops

    def agencies(self):
        return [i.get('agencyName') for i in self._transit_legs()]

