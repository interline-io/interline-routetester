import os
import unittest
import json
import math

from routetester.checkotp import *
from routetester.trip import *
from routetester.util import *        

def get_response():
    with open('tests/otp.json') as f:
        data = json.load(f)
    return OTPResponse(
        response=data, 
        status_code=200, 
        response_time=0.5,
        errors=[]
    )

class TestOTPResponse(unittest.TestCase):
    def test_itins(self):
        r = get_response()
        itins = r.itins()
        self.assertEquals(len(itins), 3)

class TestOTPItinerary(unittest.TestCase):
    def test_overall_duration(self):
        r = get_response().itins()[0]
        assert_approx_equal(r.overall_duration(), 3558)
    
    def test_overall_distance(self):
        r = get_response().itins()[0]
        assert_approx_equal(r.overall_distance(), 11267.54167)
    
    def test_walking_distance(self):
        r = get_response().itins()[0]
        assert_approx_equal(r.walking_distance(), 158.289)
    
    def test_routes(self):
        r = get_response().itins()[0]
        expect = set(['15', '22'])
        self.assertEquals(set(r.routes()), expect)

    def test_stops(self):
        r = get_response().itins()[0]
        expect = set([
            'Victoria Quay',
            'Snowsports Centre',
            'Princes Street (Stop PP)'
        ])
        self.assertEquals(set(r.stops()), expect)
    
    def test_trips(self):
        r = get_response().itins()[0]
        expect = set([
            '1:VJa073c92f2a667e84cfb9d968ca09a52ae400043b',
            '1:VJa43b619445ef7c5b0f87fe1808fd6b5fdd9e98e0'
        ])
        self.assertEquals(set(r.trips()), expect)
    
    def test_agencies(self):
        r = get_response().itins()[0]
        expect = set(['Lothian Buses'])
        self.assertEquals(set(r.agencies()), expect)

