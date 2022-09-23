import os
import os.path as op
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial

from .logger import LOGGER

CERTS_DIR = "certs"
CACERT_PATH = op.join(CERTS_DIR, "cacert.crt")
CAKEY_PATH = op.join(CERTS_DIR, "cakey.key")
CERTKEY_PATH = op.join(CERTS_DIR, "cert.key")

def check_certificates(directory):
    return op.exists(CACERT_PATH) and op.exists(CAKEY_PATH) and op.exists(CERTKEY_PATH)

def generate_certificates(directory):
    ca_name = "Autoprox CA"
    if not op.exists(directory):
        os.mkdir(directory)
    subprocess.run(['openssl', 'genrsa', '-out', CERTKEY_PATH, '2048'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    subprocess.run(['openssl', 'genrsa', '-out', CAKEY_PATH, '2048'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    subprocess.run(['openssl', 'req', '-new', '-x509', '-days', '3650', '-key', CAKEY_PATH, '-out', CACERT_PATH, '-subj', f"/CN={ca_name}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


class ProxyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, ast, *args, **kwargs):
        self.filter_ast = ast
        super().__init__(*args, **kwargs)

    def do_CONNECT(self):
        LOGGER.DEBUG("hola")

    def do_GET(self):
        if self.path == "http://autoprox/":
            self.send_file("certs/cacert.crt")
            return


    def send_file(self, path):
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Length", len(data))
        self.send_header("Content-Disposition", f"attachment; filename={op.basename(path)}")
        self.end_headers()
        self.wfile.write(data)

class Proxy:
    def __init__(self, bind, port):
        if not check_certificates(CERTS_DIR):
            LOGGER.INFO("Creating certificates")
            generate_certificates(CERTS_DIR)

        self.bind = bind
        self.port = port

    def set_config_file(self, src):
        pass

    def run(self):
        address = (self.bind, self.port)
        try:
            handler = partial(ProxyRequestHandler, "test")

            LOGGER.INFO("Serving proxy on {}:{}", *address)
            httpd = HTTPServer(address, handler)
            httpd.serve_forever()
        except KeyboardInterrupt:
            LOGGER.ERROR("Shutting down proxy")
            httpd.shutdown()
            httpd.server_close()
