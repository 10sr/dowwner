#!/usr/bin/env python3

import os

from http.server import HTTPServer, BaseHTTPRequestHandler

class DowwnerHTTPRH(BaseHTTPRequestHandler):
    # http://wiki.python.org/moin/BaseHttpServer
    def do_HEAD(self):
        if self.path.endswith(".md"):
            self.send_response(302)
            self.send_header("Location", self.path.replace(".md", ".html"))
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        return

    def do_GET(self):
        # print(self.headers)
        self.do_HEAD()
        if not self.path.endswith(".md"):
            self.wfile.write(b"<em>dowwner</em><br />")
            self.wfile.write(self.path.encode())
        return

class DowwnerHTTPS(HTTPServer):
    pass

def start(port=2505, rootdir=os.getcwd()):
    host = ""
    httpd = DowwnerHTTPS((host, port), DowwnerHTTPRH)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server terminated.")
    return
