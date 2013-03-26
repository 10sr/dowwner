#!/usr/bin/env python3

import sys
import os
# from pprint import pprint

import cgi


def print_redirect(p):
    print("Status: 302 Found")
    print("Location: http://{}{}".format(os.environ["SERVER_NAME"], p))
    return

def main(rootdir, tb=True):
    if tb:
        import cgitb
        cgitb.enable()

    try:
        path_ = os.environ["PATH_INFO"]
    except KeyError:
        print_redirect(os.environ["REQUEST_URI"] + "/")
        print()
        return

    if path_ == "/" and not os.environ["REQUEST_URI"].endswith("/"):
        print_redirect(os.environ["REQUEST_URI"] + "/")
        print()
        return

    try:
        query = os.environ["QUERY_STRING"]
        path_ = "?".join((path_, query))
    except KeyError:
        pass

    met = os.environ["REQUEST_METHOD"]

    from dowwner.dowwner import Dowwner
    d = Dowwner(rootdir)

    if met == "GET" or met == "HEAD":
        c = d.get(path_)
        pass
    elif met == "POST":
        form = cgi.FieldStorage(keep_blank_values=True)
        c = d.post(path_, form)

    if c.redirect_r:
        print_redirect(os.path.join(os.path.dirname(os.environ["REQUEST_URI"]),
                                    c.redirect))
        print()
        return

    print("Status: 200 OK")
    print("Content-Type: text/html")
    print("", flush=True)
    if met != "HEAD":
        sys.stdout.buffer.write(bytes(c))
        # _debug()
    return

def _debug():
    cgi.print_environ()
    cgi.print_environ_usage()
    cgi.print_directory()
    return
