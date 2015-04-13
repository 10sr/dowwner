#!/usr/bin/env python3

from __future__ import absolute_import

import os
import logging

try:
    from http.server import HTTPServer, BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from dowwner import __version__
from dowwner.dowwner import Dowwner

logger = logging.getLogger(__name__)


class DowwnerHTTPRH(BaseHTTPRequestHandler):
    # http://wiki.python.org/moin/BaseHttpServer

    def log_error(self, format, *args):
        logger.error(format % args)
        return

    def log_message(self, format, *args):
        logger.info(format % args)
        return

    def do_HEAD(self):
        if not self.server.dowwner_is_get_allowed(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        pathstr, q, query = self.path.partition("?")
        return self.__do("head", pathstr, query)

    def do_GET(self):
        if not self.server.dowwner_is_get_allowed(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        pathstr, q, query = self.path.partition("?")
        try:
            cachetime = self.headers["If-Modified-Since"]
        except KeyError:
            cachetime = None
        return self.__do("GET", pathstr, query, cachetime)

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

        if content is not None:
            content, encoding = self.__compress_body(content)
            headers["Content-Length"] = str(len(content))
            if encoding:
                headers["Content-Encoding"] = encoding

        self.send_response(status, message)
        for k, v in headers.items():
            self.send_header(k, v)
        if redirect is not None:
            self.__send_location(redirect)
        self.end_headers()

        if content and met.lower() != "head":
            self.wfile.write(content)
        return

    def __compress_body(self, b):
        if len(b) == 0:
            return (b, None)

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
        if not self.server.dowwner_is_post_allowed(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        pathstr, q, query = self.path.partition("?")
        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)
        pathstr, q, query = self.path.partition("?")

        return self.__do("POST", pathstr, query, data=data)


class DowwnerHTTPS(HTTPServer):
    server_version = "Dowwner/" + __version__
    # shoud i use HTTP/1.1 ? but i dont fully understand it...
    protocol_version = "HTTP/1.0"

    def __init__(self, rootdir, debug, *args, **kargs):
        self.dowwner = Dowwner(rootdir, debug)
        return HTTPServer.__init__(self, *args, **kargs)

    def dowwner_is_get_allowed(self, addr):
        return self.dowwner.is_get_allowed(addr)

    def dowwner_is_post_allowed(self, addr):
        return self.dowwner.is_post_allowed(addr)


class Server():
    """Wrapper of DowwnerHTTPS."""
    def __init__(self, port=2505, rootdir=os.getcwd(), debug=False):
        host = ""
        self.httpd = DowwnerHTTPS(rootdir, debug, (host, port), DowwnerHTTPRH)
        self.debug = debug
        self.logger = logger
        return

    def start(self):
        """Start server. This method returns when self.stop() is called."""
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        self.logger.warning("Server terminated.")
        return

    def stop(self):
        self.httpd.shutdown()
        return
