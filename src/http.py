from urllib.parse import urlsplit
import http.client as httpc

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
    def from_dict(cls, http_dict):
        http = cls()
        http.address = http_dict["address"]
        http.request_version = http_dict["request_version"]
        http.command = http_dict["command"]
        http.headers = http_dict["headers"]
        http.body = http_dict["body"]
        url = urlsplit(http_dict["path"])
        print("PAAATH", url)
        http.scheme, http.netloc, http.path = url.scheme, url.netloc, f"{url.path}?{url.query}" if url.query else url.path
        return http

    def modify(self, ast):
        pass

    def is_https(self):
        return self.scheme.lower() == "https"

    def request(self):
        # if self.is_https():
        #     connection = httplib.HTTPSConnection(self.netloc, timeout=5)
        print(self.netloc)
        connection = httpc.HTTPSConnection(self.netloc, timeout=5)
        print(self.command, self.path, self.body, self.headers)
        connection.request(self.command, self.path, self.body, self.headers)
        response = connection.getresponse()

        # Creamos la respuesta
        response_dict = {
            "version": response.version,
            "status_code": response.status,
            "reason": response.reason,
            "headers": dict((h, v) for h, v in response.getheaders()),
            "body": response.read()
        }
        http_response = HTTPResponse.from_dict(response_dict)
        return http_response

    def __repr__(self):
        req_str = f"{self.scheme.upper()} Request from {self.address[0]}:{self.address[1]}\n\n"
        req_str += f"{self.command} {self.path} {self.request_version}\n"
        for h, v in self.headers.items():
            req_str += f"{h}: {v}\n"
        req_str += f"\n{self.body.decode('utf-8') if self.body else ''}"
        return req_str

class HTTPResponse:
    def __init__(self):
        self.version = None
        self.status_code = None
        self.reason = None
        self.headers = dict()
        self.body = str()

    @classmethod
    def from_dict(cls, http_dict):
        http = cls()
        http.version = {10: 'HTTP/1.0', 11: 'HTTP/1.1'}[http_dict["version"]]
        http.status_code = http_dict["status_code"]
        http.reason = http_dict["reason"]
        http.headers = http_dict["headers"]
        http.body = http_dict["body"]
        return http

    def write(self, req_handler):
        req_handler.wfile.write(f"{self.version} {self.status_code} {self.reason}\r\n".encode())
        for h, v in self.headers.items():
            req_handler.wfile.write(f"{h}: {v}\r\n".encode())
        req_handler.wfile.write(f"\r\n".encode())
        req_handler.wfile.write(self.body)
        req_handler.wfile.flush()

    def __repr__(self):
        res_str = f"{self.version} {self.status_code} {self.reason}\n"
        for h, v in self.headers.items():
            res_str += f"{h}: {v}\n"
        res_str += f"\n{self.body.decode('utf-8')}"
        return res_str
