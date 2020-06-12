import sys

from .util import when
from .geom import haversine

DEFAULTWHEN = 'next monday at 8am'

class Trip(object):
    def __init__(self, geometry, properties, id=None, when=None, **kwargs):
        self.id = id
        self.geometry = geometry
        self.properties = properties

    def as_feature(self):
        return {
            "type": "Feature",
            "properties": self.properties,
            "geometry": self.geometry,
            "id": self.id
        }

    def haversineDistance(self):
        o, d = self.origin(), self.destination()
        return haversine(o[0], o[1], d[0], d[1])

    def get(self, key, default=None):
        return self.properties.get(key, default)

    def update(self, **kwargs):
        self.properties.update(**kwargs)

    def origin(self):
        return self.geometry['coordinates'][0]

    def destination(self):
        return self.geometry['coordinates'][1]

    def mode(self):
        return self.get('mode')

    def when(self):
        return when(self.get('when', DEFAULTWHEN), tz=self.get('whentz'))

    def expect_status_code(self):
        return self.get('httpStatusCode')

    def expect_duration(self):
        return self.get('minDuration', 0), self.get('maxDuration')

    def expect_overall_distance(self):
        return self.get('minOverallDistance', 0), self.get('maxOverallDistance')

    def expect_walking_distance(self):
        return self.get('minWalkingDistance'), self.get('maxWalkingDistance')

    def expect_transit_legs(self):
        return self.get('minTransitLegs'), self.get('maxTransitLegs')
    
    def expect_routes(self):
        incl = set(self.get('includesRoute', '').split(',')) - set([''])
        excl = set(self.get('excludesRoute', '').split(',')) - set([''])
        return incl, excl

    def expect_trips(self):
        incl = set(self.get('includesTrip', '').split(',')) - set([''])
        excl = set(self.get('excludesTrip', '').split(',')) - set([''])
        return incl, excl

    def expect_stops(self):
        incl = set(self.get('includesStop', '').split(',')) - set([''])
        excl = set(self.get('excludesStop', '').split(',')) - set([''])
        return incl, excl

    def expect_agencies(self):
        incl = set(self.get('includesAgency', '').split(',')) - set([''])
        excl = set(self.get('excludesAgency', '').split(',')) - set([''])
        return incl, excl
