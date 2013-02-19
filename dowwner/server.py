#!/usr/bin/env python3

import os
import sys
from traceback import format_exception, print_exception

from http.server import HTTPServer, BaseHTTPRequestHandler

from dowwner.pages import Pages

class DowwnerHTTPRH(BaseHTTPRequestHandler):
    # http://wiki.python.org/moin/BaseHttpServer
    def do_HEAD(self):
        self.do_GET(True)
        return

    def do_GET(self, head_only=False):
        try:
            return self.__try_do_GET(head_only)
        except Exception as e:
            return self.__send_500(sys.exc_info(), head_only)

    def __try_do_GET(self, head_only=False):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        p = self.server.dowwner_pages.get(self.path)
        if p.redirect is not None:
            self.send_response(302)
            self.send_header("Location", p.redirect)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if not head_only:
                self.wfile.write(p.content)
        return

    def do_POST(self):
        try:
            return self.__try_do_POST()
        except Exception as e:
            return self.__send_500(sys.exc_info())

    def __try_do_POST(self):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        length = int(self.headers["Content-Length"])
        data = self.rfile.read(length)
        rt = self.server.dowwner_pages.post(self.path, data)
        if rt:
            self.send_response(302)
            self.send_header("Location", rt.redirect)
            self.end_headers()
            self.wfile.write(str(data).encode())
        return

    def __send_500(self, exc_info, head_only=False):
        self.send_error(500)
        self.end_headers()
        if not head_only:
            self.wfile.write(
                "<br />\n".join(format_exception(*exc_info)).encode())
        print_exception(*exc_info)
        return

class DowwnerHTTPS(HTTPServer):
    def __init__(self, rootdir, *args, **kargs):
        self.dowwner_pages = Pages(rootdir)
        return HTTPServer.__init__(self, *args, **kargs)

    def dowwner_verify(self, addr):
        return self.dowwner_pages.verify_addr(addr)

def start(port=2505, rootdir=os.getcwd()):
    host = ""
    httpd = DowwnerHTTPS(rootdir, (host, port), DowwnerHTTPRH)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Server terminated.")
    return
