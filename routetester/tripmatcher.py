import sys
from .util import join

class TripError(Exception):
    pass

class TripMatcher(object):
    def check(self, trip, response):
        errors = []
        errors += self.check_status_code(trip, response)
        itinerrors = [self.check_itin(trip, i) for i in response.itins()]
        itinerrors = sorted(itinerrors, key=lambda x:len(x))
        if itinerrors:
            errors += itinerrors[0]
        else:
            errors.append(TripError("No itineraries returned"))
        return errors

    def check_itin(self, trip, itin):
        errors = []
        errors += self.check_duration(trip, itin)
        errors += self.check_overall_distance(trip, itin)
        errors += self.check_walking_distance(trip, itin)
        errors += self.check_transit_legs(trip, itin)
        errors += self.check_routes(trip, itin)
        errors += self.check_trips(trip, itin)
        errors += self.check_stops(trip, itin)
        errors += self.check_agencies(trip, itin)
        return errors

    def check_status_code(self, trip, response):
        errors = []
        expect = trip.expect_status_code() or 200
        found = response.status_code
        if expect != found:
            errors.append(TripError("Incorrect status_code; got %s expected %s"%(found, expect)))
        return errors

    def _check_bounds(self, arange, value, key=''):
        errors = []
        amin, amax = arange
        amin = float(amin or 0)
        amax = float(amax or float("inf"))
        # print("%s: %s < %s < %s"%(key, amin, value, amax))
        if value < amin:
            errors.append(TripError("%s out of bounds: got %s, expected min %s"%(key, value, amin)))
        elif value > amax:
            errors.append(TripError("%s out of bounds: got %s, expected max %s"%(key, value, amax)))
        return errors

    def _check_contains(self, inclexcl, value, key='value'):
        errors = []
        incl, excl = inclexcl
        value = set(value)
        found = incl & value
        disallowed = excl & value
        # print("key %s: incl: %s excl: %s value: %s"%(key, incl, excl, value))
        if incl and not found:
            errors.append(TripError("Missing %s: got %s expected %s"%(key, join(value), join(incl))))
        if disallowed:
            errors.append(TripError("Found disallowed %s: got %s, disallowed %s"%(key, join(value), join(disallowed))))
        return errors

    def check_duration(self, trip, itin):
        return self._check_bounds(
            trip.expect_duration(),
            itin.overall_duration(),
            'Duration'
        )

    def check_overall_distance(self, trip, itin):
        return self._check_bounds(
            trip.expect_overall_distance(),
            itin.overall_distance(),
            'Overall distance'
        )

    def check_walking_distance(self, trip, itin):
        return self._check_bounds(
            trip.expect_walking_distance(),
            itin.walking_distance(),
            'Walking distance'
        )

    def check_transit_legs(self, trip, itin):
        return self._check_bounds(
            trip.expect_transit_legs(),
            len(itin._transit_legs()),
            'Transit legs'
        )

    def check_routes(self, trip, itin):
        return self._check_contains(
            trip.expect_routes(),
            itin.routes(),
            'route'
        )

    def check_trips(self, trip, itin):
        return self._check_contains(
            trip.expect_trips(),
            itin.trips(),
            'trip'
        )

    def check_stops(self, trip, itin):
        return self._check_contains(
            trip.expect_stops(),
            itin.stops(),
            'stop'
        )

    def check_agencies(self, trip, itin):
        return self._check_contains(
            trip.expect_agencies(),
            itin.agencies(),
            'agency'
        )

