#!/usr/bin/env python3

import sys
import os
# from pprint import pprint

import cgi

from dowwner import exc

def print_redirect(p):
    print("Status: 302 Found")
    print("Location: http://{}{}{}".format(os.environ["SERVER_NAME"],
                                         os.environ["SCRIPT_NAME"],
                                         p))
    return

def main(rootdir, tb=True):
    if tb:
        import cgitb
        cgitb.enable()

    try:
        path_ = os.environ["PATH_INFO"]
    except KeyError:
        print_redirect("/")
        print()
        return

    if path_ == "": # and not os.environ["REQUEST_URI"].endswith("/"):
        # this is not good because REQUEST_URI is not assured to exist,
        print_redirect("/")
        print()
        return

    try:
        query = os.environ["QUERY_STRING"]
        if query:
            path_ = "?".join((path_, query))
    except KeyError:
        pass

    met = os.environ["REQUEST_METHOD"]

    from dowwner.dowwner import Dowwner
    d = Dowwner(rootdir)

    try:
        if met == "GET" or met == "HEAD":
            c = d.get(path_)
            pass
        elif met == "POST":
            form = cgi.FieldStorage(keep_blank_values=True)
            c = d.post(path_, form)
    except exc.PageNameError as e:
        print("Status: 403 Forbidden")
        print("")
        print(str(e))
        return

    if c.redirect_r:
        print_redirect(os.path.join(os.path.dirname(path_),
                                    c.redirect))
        print()
        return

    print("Status: 200 OK")
    print("Content-Type: " + c.type) # ;charset=utf-8
    if c.filename:
        print("Content-Disposition: attachment; filename={}".format(c.filename))
    body = bytes(c)
    print("Content-Length: {}".format(len(body)))
    print("", flush=True)
    if met != "HEAD":
        sys.stdout.buffer.write(body)
        #_debug()
    return

def _debug():
    print("Status: 200 OK")
    print("Content-Type: text/html")
    print()
    cgi.print_environ()
    cgi.print_environ_usage()
    cgi.print_directory()
    return
