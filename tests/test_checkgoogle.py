import os
import unittest
import json
import math

from routetester.checkgoogle import *
from routetester.trip import *
from routetester.util import *        

def get_response():
    with open('tests/google.json') as f:
        data = json.load(f)
    return GoogleResponse(
        response=data, 
        status_code=200, 
        response_time=0.5,
        errors=[]
    )

class Test_gettimegm(unittest.TestCase):
    def test_get_timegm(self):
        pass

class TestGoogleResponse(unittest.TestCase):
    def test_itins(self):
        r = get_response()
        itins = r.itins()
        self.assertEquals(len(itins), 1)

class TestGoogleItinerary(unittest.TestCase):
    def test_overall_duration(self):
        r = get_response().itins()[0]
        assert_approx_equal(r.overall_duration(), 3715)
    
    def test_overall_distance(self):
        r = get_response().itins()[0]
        assert_approx_equal(r.overall_distance(), 11368)
    
    def test_walking_distance(self):
        r = get_response().itins()[0]
        assert_approx_equal(r.walking_distance(), 381.0)
    
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
        ])
        self.assertEquals(set(r.trips()), expect)
    
    def test_agencies(self):
        r = get_response().itins()[0]
        expect = set(['Lothian Buses'])
        self.assertEquals(set(r.agencies()), expect)

