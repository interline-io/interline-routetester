import os
import unittest
import json
import math

from routetester.checkotp import *
from routetester.checker import *
from routetester.trip import *
from routetester.util import *        

class TestTripMatcher(unittest.TestCase):
    def get_trip(self):
        c = Checker(host='http://example.com', request_cls=None)
        c.load('tests/trip.json')
        return c.queue[0]

    def get_response(self):
        with open('tests/otp.response.json') as f:
            data = json.load(f)
        return OTPResponse(
            response=data, 
            status_code=200, 
            response_time=0.5,
            errors=[]
        )

    def test_overall(self):
        trip, response = self.get_trip(), self.get_response()
        errors = TripMatcher().check(trip, response)
        self.assertEquals(errors, [])

    def test_status_code(self):
        trip, response = self.get_trip(), self.get_response()
        errors = TripMatcher().check_status_code(trip, response)
        self.assertEquals(errors, [])

    def test_check_duration(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_duration(trip, itin)
        self.assertEquals(errors, [])

    def test_overall_distance(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_overall_distance(trip, itin)
        self.assertEquals(errors, [])        

    def test_walking_distance(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_walking_distance(trip, itin)
        self.assertEquals(errors, [])

    def test_transit_legs(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_transit_legs(trip, itin)
        self.assertEquals(errors, [])

    def test_routes(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_routes(trip, itin)
        self.assertEquals(errors, [])
      
    def test_stops(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_stops(trip, itin)
        self.assertEquals(errors, [])

    def test_trips(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_trips(trip, itin)
        self.assertEquals(errors, [])

    def test_agencies(self):
        trip, itin = self.get_trip(), self.get_response().itins()[0]
        errors = TripMatcher().check_agencies(trip, itin)
        self.assertEquals(errors, [])
    
