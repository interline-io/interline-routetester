class Request(object):
    REQUEST_CLS = {}

    @classmethod
    def register(cls, name):
        def r(cls2):
            cls.REQUEST_CLS[name] = cls2
            return cls2
        return r

    @classmethod
    def get_cls(cls, name):
        return cls.REQUEST_CLS.get(name, None)

    def __init__(self, host):
        self.host = host

    def url(self, trip):
        raise NotImplementedError

    def request(self, trip):
        raise NotImplementedError

