#!/usr/bin/env python3

import os

from urllib import parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from dowwner.pages import Pages
from dowwner.editor import Editor

class DowwnerHTTPRH(BaseHTTPRequestHandler):
    # http://wiki.python.org/moin/BaseHttpServer
    def do_HEAD(self):
        self.do_GET(True)
        return

    def do_GET(self, head_only=False):
        try:
            return self.__try_do_GET(head_only)
        except Exception as e:
            self.send_error(500)
            self.end_headers()
            if not head_only:
                self.wfile.write(str(e).encode())
            return

    def __try_do_GET(self, head_only=False):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        if self.path.startswith("/.edit/"):
            # edit page
            rpath = self.path.replace("/.edit/", "", 1)
            p = self.server.dowwner_editor(rpath)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if not head_only:
                self.wfile.write(p.content)
            return

        if self.path.startswith("/.get/"):
            rpath = self.path.replace("/.get/", "", 1)
            data = parse.parse_qs(rpath.partition("?")[2])
            print(data)
            self.send_response(302)
            self.send_header("Location", ("/" + data["pagename"][0]))
            self.end_headers()
            return

        rpath = self.path.lstrip("/")
        dirname, basename = os.path.split(rpath)
        p = self.server.dowwner_pages.get(rpath)
        if p.exists:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # print(p.content)
            if not head_only:
                self.wfile.write(p.content)
        else:
            # redirect to edit page
            assert self.path != "/"
            self.send_response(302)
            self.send_header("Location", ("/" + ".edit/" + rpath))
            self.end_headers()
            if not head_only:
                self.wfile.write(p.content)
        return

    def do_POST(self):
        try:
            return self.__try_do_POST()
        except Exception as e:
            self.send_error(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
            return

    def __try_do_POST(self):
        if not self.server.dowwner_verify(self.client_address[0]):
            self.send_error(403)
            self.end_headers()
            return

        assert self.path.startswith("/.save/")
        rpath = self.path.replace("/.save/", "", 1)
        length = int(self.headers["Content-Length"])
        # cannot use parse_qs without decoding when japanese contained...
        data = parse.parse_qs(self.rfile.read(length).decode(),
                              keep_blank_values=True)
        rt = self.server.dowwner_pages.post(rpath, data["content"][0])
        if rt:
            self.send_response(302)
            self.send_header("Location", "/" + rpath)
            self.end_headers()
            self.wfile.write(str(data).encode())
        # self.send_response(200)
        # self.send_header("Content-type", "text/html")
        # self.end_headers()
        # self.wfile.write(b"success!<br />")
        # self.wfile.write(str(data).encode())
        return

class DowwnerHTTPS(HTTPServer):
    def __init__(self, rootdir, *args, **kargs):
        self.dowwner_pages = Pages(rootdir)
        self.dowwner_editor = Editor
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
