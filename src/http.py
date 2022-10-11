class HTTPRequest:
    def __init__(self):
        self.address = None
        self.request_version = None
        self.command = None
        self.scheme = None
        self.netloc = None
        self.path = None
        self.query = None
        self.headers = dict()
        self.body = str()

    @classmethod
    def from_dict():
        pass
