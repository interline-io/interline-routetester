import os
import unittest
import json
import math

from routetester.checker import *
from routetester.trip import *
from routetester.util import *        

class TestTrip(unittest.TestCase):
    def get_trip(self):
        c = Checker(host='http://example.com', request_cls=None)
        c.load('tests/trip.json')
        assert len(c.queue) == 1
        return c.queue[0]

    def test_status_code(self):
        trip = self.get_trip()
        expect = 200
        found = trip.expect_status_code()
        self.assertEqual(expect, found)

    def test_origin(self):
        trip = self.get_trip()
        expect = [-3.31984, 55.90909]
        origin = trip.origin()
        assert_approx_equal(origin[0], expect[0])
        assert_approx_equal(origin[1], expect[1])

    def test_destination(self):
        trip = self.get_trip()
        expect = [-3.23389, 55.96309]
        dest = trip.destination()
        assert_approx_equal(dest[0], expect[0])
        assert_approx_equal(dest[1], expect[1])

    def test_expect_duration(self):
        trip = self.get_trip()
        amin, amax = trip.expect_duration()
        assert_approx_equal(amin, 3000.0)
        assert_approx_equal(amax, 3100.0)

    def test_expect_overall_distance(self):
        trip = self.get_trip()
        amin, amax = trip.expect_overall_distance()
        assert_approx_equal(amin, 10000.0)
        assert_approx_equal(amax, 12000.0)

    def test_expect_walking_distance(self):
        trip = self.get_trip()
        amin, amax = trip.expect_walking_distance()
        assert_approx_equal(amin, 300.0)
        assert_approx_equal(amax, 400.0)

    def test_expect_transit_legs(self):
        trip = self.get_trip()
        amin, amax = trip.expect_transit_legs()
        assert_approx_equal(amin, 2)
        assert_approx_equal(amax, 4)
        
    def test_expect_routes(self):
        trip = self.get_trip()
        incl, excl = trip.expect_routes()
        self.assertEquals(incl, set(['25','47']))
        self.assertEquals(excl, set(['C', 'D']))
     
    def test_expect_stops(self):
        trip = self.get_trip()
        incl, excl = trip.expect_stops()
        self.assertEquals(incl, set(["West Woods","Heriot Watt Campus"]))
        self.assertEquals(excl, set(['Y', 'Z']))
     
    def test_expect_agencies(self):
        trip = self.get_trip()
        incl, excl = trip.expect_agencies()
        self.assertEquals(incl, set(['Lothian Buses']))
        self.assertEquals(excl, set(['Ferry', 'Helicopter']))

    def test_expect_trips(self):
        trip = self.get_trip()
        incl, excl = trip.expect_trips()
        self.assertEquals(incl, set(['1:VJ8181966ca170f6c376764b024a53084d1079791a']))
        self.assertEquals(excl, set(['bar']))
