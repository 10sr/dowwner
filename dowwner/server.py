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
        self.do_GET(True)
        return

    def do_GET(self, head_only=False):
        try:
            return self.__try_do_GET(head_only)
        except Exception as e:
            if isinstance(e, exc.PageNameError):
                return self.__send_err(403, sys.exc_info(), head_only)
            else:
                return self.__send_err(500, sys.exc_info(), head_only)

    def __compress_body(self, b):
        # encodings = self.headers["Accept-Encoding"].split(",")
        # for e in encodings:
        return (b, None)

    def __send_location(self, s):
        newpath = os.path.join(os.path.dirname(self.path), s)
        self.send_header("Location",
                         "http://{}{}".format(self.headers["Host"], newpath))
        return

    def __try_do_GET(self, head_only=False):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        c = self.server.dowwner.get(self.path)
        if c.redirect is not None:
            self.send_response(302)
            self.__send_location(c.redirect)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", c.type)
            body, encoding = self.__compress_body(bytes(c))
            self.send_header("Content-Length", str(len(body)))
            if encoding:
                self.send_header("Content-Encoding", encoding)
            self.end_headers()
            if not head_only:
                self.wfile.write(body)
        return

    def do_POST(self):
        try:
            return self.__try_do_POST()
        except Exception as e:
            if isinstance(e, exc.PageNameError):
                return self.__send_err(403, sys.exc_info())
            else:
                return self.__send_err(500, sys.exc_info())

    def __try_do_POST(self):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)
        rt = self.server.dowwner.post(self.path, data)
        if rt:
            self.send_response(302)
            self.__send_location(rt.redirect)
            self.end_headers()
            #self.wfile.write(str(data).encode())
        return

    def __send_err(self, num, exc_info, head_only=False):
        self.send_error(num)
        self.end_headers()
        if not head_only:
            self.wfile.write(
                "<br />\n".join(format_exception(*exc_info)).encode())
        print_exception(*exc_info)
        return

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
