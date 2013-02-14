#!/usr/bin/env python3

import os

from http.server import HTTPServer, BaseHTTPRequestHandler
from dowwner.contents import Contents

class DowwnerHTTPRH(BaseHTTPRequestHandler):
    # http://wiki.python.org/moin/BaseHttpServer
    def do_HEAD(self):
        self.do_GET(True)
        return

    def do_GET(self, head_only=False):
        c = self.server.dowwner_contents.get(self)
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
        elif c.exists:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if not head_only:
                self.wfile.write(c.content)
        else:
            self.send_response(302)
            self.send_header("Location", self.path + ".md")
            self.end_headers()
            if not head_only:
                self.wfile.write(c.content)
        return

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        content = self.rfile.read(length)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"success!<br />")
        self.wfile.write(content)
        return

class DowwnerHTTPS(HTTPServer):
    def __init__(self, rootdir, *args, **kargs):
        self.dowwner_contents = Contents(rootdir)
        return HTTPServer.__init__(self, *args, **kargs)

    def dowwner_verify(self, addr):
        return self.dowwner_contents.verify_addr(addr)

def start(port=2505, rootdir=os.getcwd()):
    host = ""
    httpd = DowwnerHTTPS(rootdir, (host, port), DowwnerHTTPRH)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    print("Server terminated.")
    return

def stop(rootdir=os.getcwd()):
    return
