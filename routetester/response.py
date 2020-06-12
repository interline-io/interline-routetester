class Response(object):
    def __init__(self, response, status_code=None, response_time=None, errors=None, url=None):
        self.status_code = status_code
        self.response = response or {}
        self.response_time = response_time or 0.0
        self.errors = errors or []
        self.url = url

    def itins(self):
        return []

    def valid(self):
        return len(self.itins()) > 0

    def json(self):
        return {
            "status_code": self.status_code,
            "response_time": self.response_time,
            "errors": [str(i) for i in self.errors],
            "url": self.url,
            "itineraries": [i.json() for i in self.itins()],
            "request_cls": self.__class__.__name__,
            # "response": self.response
        }

class Itinerary(object):
    def __init__(self, data):
        self.data = data or {}

    def json(self):
        return {
            "overall_duration": self.overall_duration(),
            "overall_distance": self.overall_distance(),
            "walking_distance": self.walking_distance(),
            "routes": list(set(self.routes())),
            "trips": list(set(self.trips())),
            "stops": list(set(self.stops())),
            "agencies": list(set(self.agencies()))
        }

    def valid(self):
        return True

    def get(self, key, default=None):
        return self.data.get(key, default)

    def _walking_legs(self):
        return []

    def _transit_legs(self):
        return []

    def overall_duration(self):
        raise NotImplementedError

    def overall_distance(self):
        raise NotImplementedError

    def walking_distance(self):
        raise NotImplementedError

    def routes(self):
        raise NotImplementedError

    def trips(self):
        raise NotImplementedError

    def stops(self):
        raise NotImplementedError

    def agencies(self):
        raise NotImplementedError
