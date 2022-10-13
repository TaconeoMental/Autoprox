import os
import os.path as op
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
import time
import ssl
from src.logger import LOGGER
from src.builder import Builder
from src.http import HTTPRequest

CERTS_DIR = "certs"
WEB_CERTS_DIR = op.join(CERTS_DIR, "web/")
CACERT_PATH = op.join(CERTS_DIR, "cacert.crt")
CAKEY_PATH = op.join(CERTS_DIR, "cakey.key")
CERTKEY_PATH = op.join(CERTS_DIR, "cert.key")

def check_certificates(directory):
    return op.exists(CACERT_PATH) and op.exists(CAKEY_PATH) and op.exists(CERTKEY_PATH)

def generate_certificates(directory):
    ca_name = "Autoprox CA"
    if not op.exists(directory):
        os.mkdir(directory)
        os.mkdir(WEB_CERTS_DIR)
    subprocess.run(['openssl', 'genrsa', '-out', CERTKEY_PATH, '2048'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Generamos llave privada para CA
    subprocess.run(['openssl', 'genrsa', '-out', CAKEY_PATH, '2048'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    # Certificado root
    subprocess.run(['openssl', 'req', '-new', '-x509', '-days', '365', '-key', CAKEY_PATH, '-out', CACERT_PATH, '-subj', f"/CN={ca_name}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


class ProxyRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, p_version, ast, *args, **kwargs):
        self.protocol_version = p_version
        self.ast = ast
        super().__init__(*args, **kwargs)

    def do_CONNECT(self):
        host = self.path.split(":")[0]
        new_cert_path = op.join(WEB_CERTS_DIR, f"{host}.crt")
        if not op.exists(new_cert_path):
            print("iai")
            epoch = int(time.time() * 1000)
            s1 = subprocess.run(['openssl', 'req', '-new', '-key', CERTKEY_PATH, '-subj', f"/CN={host}"],
                           capture_output=True, check=True)
            subprocess.run(['openssl', 'x509', '-req', '-days', '3650', '-CA', CACERT_PATH, '-CAkey', CAKEY_PATH, '-set_serial', str(epoch), '-out', new_cert_path],
                           input=s1.stdout, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        self.wfile.write(f"{self.protocol_version} 200 Connection Established\r\n\r\n".encode("utf-8"))
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.load_cert_chain(new_cert_path, CERTKEY_PATH)
        self.connection = context.wrap_socket(sock=self.connection,
                                              server_side=True)
        self.rfile = self.connection.makefile("rb", self.rbufsize)
        self.wfile = self.connection.makefile("wb", self.wbufsize)

        if self.protocol_version == "HTTP/1.1" and self.headers.get('Proxy-Connection', '').lower() != "close":
            self.close_connection = 0
        else:
            self.close_connection = 1

    def do_GET(self):
        if self.path == "http://autoprox/":
            self.send_file(CACERT_PATH)
            return

        parsed_headers = self.parse_headers(self.headers)

        url_path = self.path
        if self.path[0] == '/':
            if isinstance(self.connection, ssl.SSLSocket):
                url_path = f"https://{parsed_headers['Host']}{self.path}"
            else:
                url_path = f"http://{parsed_headers['Host']}{self.path}"

        content_length = int(self.headers.get('Content-Length', 0)) # Devuelve 0 si no existe
        req_body = self.rfile.read(content_length) if content_length else None
        req_dir = {
            "address": self.client_address,
            #"protocol_version": self.protocol_version,
            "request_version": self.request_version,
            "command": self.command,
            "path": url_path,
            "headers": parsed_headers,
            "body": req_body
        }

        req = HTTPRequest.from_dict(req_dir)
        req.modify(self.ast)
        response = req.request()
        response.write(self)

        #print(req)
        #print(response)

    do_POST = do_GET

    def parse_headers(self, headers):
        p_headers = dict()
        for h in headers:
            if h:
                p_headers[h] = headers[h]
        return p_headers

    def send_file(self, path):
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Length", len(data))
        self.send_header("Content-Disposition", f"attachment; filename={op.basename(path)}")
        self.end_headers()
        self.wfile.write(data)

class Proxy:
    def __init__(self, bind, port, src):
        if not check_certificates(CERTS_DIR):
            LOGGER.INFO("Creating certificates")
            generate_certificates(CERTS_DIR)

        self.bind = bind
        self.port = port
        self.config_file = ""

        builder = Builder(src)
        self.ast = builder.run()


    def run(self):
        address = (self.bind, self.port)
        try:
            protocol_version = "HTTP/1.1"
            handler = partial(ProxyRequestHandler, protocol_version, self.ast)

            LOGGER.GOOD("Serving proxy on {}:{}", *address)
            httpd = HTTPServer(address, handler)
            httpd.serve_forever()
        except KeyboardInterrupt:
            print() # Para más placer
            LOGGER.ERROR("Shutting down proxy")
            httpd.shutdown()
            httpd.server_close()
