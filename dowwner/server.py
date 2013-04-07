#!/usr/bin/env python3

from __future__ import absolute_import

import os
import sys
from traceback import format_exception, print_exception

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from dowwner import __version__
from dowwner.dowwner import Dowwner
from dowwner import exc

class DowwnerHTTPRH(BaseHTTPRequestHandler):
    # http://wiki.python.org/moin/BaseHttpServer

    server_version = "Dowwner/" + __version__

    def do_HEAD(self):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        pathstr, q, query = self.path.partition("?")
        return self.__do("HEAD", pathstr, query)

    def do_GET(self):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        pathstr, q, query = self.path.partition("?")
        return self.__do("GET", pathstr, query)

    def __do(self, met, *args, **kargs):
        if met.lower() == "head":
            c = self.server.dowwner.req_http("get", *args, **kargs)
        else:
            c = self.server.dowwner.req_http(met, *args, **kargs)

        status = c[0]
        message = c[1]
        redirect = c[2]
        headers = c[3]
        content = c[4]

        content, encoding = self.__compress_body(content)
        headers["Content-Length"] = str(len(content))
        if encoding:
            headers["Content-Encoding"] = encoding

        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        if redirect is not None:
            self.__send_location(redirect)
        self.end_headers()

        if met.lower() != "head":
            self.wfile.write(content)
        return

    def __compress_body(self, b):
        encodings = (e.strip() for e
                     in self.headers["Accept-Encoding"].split(","))
        for e in encodings:
            if e.startswith("gzip"):
                return (self.__compress_gzip(b), "gzip")
        return (b, None)

    def __compress_gzip(self, b):
        from gzip import compress
        return compress(b)

    def __send_location(self, s):
        newpath = os.path.join(os.path.dirname(self.path), s)
        self.send_header("Location",
                         "http://{}{}".format(self.headers["Host"], newpath))
        return

    def do_POST(self):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        pathstr, q, query = self.path.partition("?")
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)
        pathstr, q, query = self.path.partition("?")

        return self.__do("POST", pathstr, query, data)

class DowwnerHTTPS(HTTPServer):
    def __init__(self, rootdir, *args, **kargs):
        self.dowwner = Dowwner(rootdir)
        return HTTPServer.__init__(self, *args, **kargs)

    def dowwner_verify(self, addr):
        return self.dowwner.verify_addr(addr)

def start(port=2505, rootdir=os.getcwd()):
    host = ""
    httpd = DowwnerHTTPS(rootdir, (host, port), DowwnerHTTPRH)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Server terminated.")
    return
